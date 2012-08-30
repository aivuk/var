{-# OPTIONS_GHC -XBangPatterns #-}

import System.Random.MWC 
import qualified System.Random as R 
import qualified Data.Vector.Unboxed as V
import Control.Monad (replicateM)

data RandVec = RV { dim  :: Int
                  , mod  :: Int
                  , rv_bounds :: (Int, Int)
                  , vals :: V.Vector Int }
    deriving (Show)

makeVec l bounds = RV (length l) (sum l) bounds (V.fromList l) 

makeRandVec n bounds g = do 
    rvl <- replicateM n (uniformR bounds g)
    return $ makeVec rvl (0, sum rvl)

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

vec_hash (RV _ m _ v) = V.sum $ V.zipWith (*) (V.map (m^) (V.enumFromTo 0 (V.length v - 1))) v

main = do
   sg <- R.getStdGen
   rs <- return $ take 256 $ R.randoms sg
   g <- initialize $ V.fromList rs
   rv <- makeRandVec 10 (0,2) g
   let num_vecs = 10000
   new_vecs <- replicateM num_vecs (changeRandVec rv g)
   return ()
 
