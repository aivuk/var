{-# OPTIONS_GHC -XBangPatterns #-}
module Main where

import System.Random.MWC 
import qualified System.Random as R 
import qualified Data.Vector.Unboxed as V
import Control.Monad (replicateM)
import qualified Data.Map as M
import Data.List (sort)

data RandVec = RV { dim  :: Int
                  , rv_mod  :: Int
                  , rv_bounds :: (Int, Int)
                  , vals :: V.Vector Int }
    deriving (Show)

makeVec l bounds = RV (length l) (sum l) bounds (V.fromList l) 

makeRandVec n bounds g = do 
    rvl <- replicateM n (uniformR bounds g)
    return $ makeVec rvl (0, sum rvl)
   
uniRandVec c d g = do
    (p:ps) <- return.sort =<< replicateM (d - 1) (uniformR (0, c) g)
    return $ vec_comps (p:ps) [p]
        where
            vec_comps (p:p':ps) vl = vec_comps (p':ps) ((p' - p):vl)
            vec_comps (p':[]) vl = (c - p'):vl   
            vec_comps [] vl = vl

changeRandVec rv@(RV _ !m !bds !v) g = do
    i <- uniformR (0, V.length v - 1) g
    let diff_i = do
            j <- uniformR (0, V.length v - 1) g 
            if j /= i 
             then return j
             else diff_i
    j <- diff_i
    let sum_ij = v V.! i + v V.! j
    r_i <- uniformR (0, sum_ij) g
    return $ rv{ vals = v V.// [ (i, r_i), (j, sum_ij - r_i) ]}

vec_hash :: RandVec -> Integer
vec_hash (RV _ m _ v) = sum $ zipWith (*) (map (mi^) [0.. lv]) ivec
    where 
        mi = fromIntegral m
        lv = fromIntegral $ V.length v - 1
        ivec = map fromIntegral $ V.toList v

save_points l m t = writeFile filename $ unlines out
   where
       out = map (\(i,j) -> (show i) ++ ", " ++ (show j)) $
                zip [1..] l
       filename = "points-mod-" ++ (show m) ++ "-" ++ (show t) ++ ".csv"
 
main = do
   sg <- R.getStdGen
   rs <- return $ take 256 $ R.randoms sg
   g <- initialize $ V.fromList rs
   rv <- makeRandVec 10 (0,20) g
   let num_vecs = 1000000
--   new_vecs <- replicateM num_vecs (changeRandVec rv g)
   new_vecs <- replicateM num_vecs (return.(RV 11 3 (0,200).(V.fromList)) =<< uniRandVec 3 11 g) 
   let hist = M.fromListWith (+) $ zip (map vec_hash new_vecs) (repeat 1)
   save_points (sort $ M.elems hist) (100) num_vecs
   return ()
 
