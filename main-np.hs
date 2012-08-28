{-# OPTIONS_GHC -XBangPatterns #-}

module Main where
import System.Random.MWC
import qualified Data.Vector.Unboxed as V
import qualified System.Random as R
import System.Environment
import Control.Monad

data Wheel = W { parts      :: !Int
               , uniSize    :: !Double
               , biggerSize :: !Double 
               , diffSize   :: !Double } 

mkWheel p inc = W p us bs ds
    where
        us = 2 * pi / fromIntegral p
        bs = (1 + inc) * us
        ds = bs - us
 
spin !w !g = do
    r <- uniformR (0, 2 * pi) g
    let (p, r') = properFraction $ r / uniSize w
    if even p || r' * (uniSize w) <= diffSize w
     then return 1
     else return 0

sumA n w g = sumA' n 0 
    where
        sumA' !n !a | n > 0 = do
                        isA <- spin w g
                        sumA' (n - 1) (a + isA) 
                    | otherwise = return a

save_points np l times = writeFile filename $ unlines out
    where
        out = map (\(i, f) -> show (2 * i) ++ ", " ++ show (f / times)) $ zip [1..] l
                  --  zip [1..] $ zipWith (/) (map fromIntegral l) [1..]
        filename = "points-" ++ (show np) ++ "-" ++ (show $ length l) ++ ".csv"

main = do
    [n, t, i] <- getArgs
    let n_parts = read n
        times = read t
        inc = read i
        w = mkWheel n_parts inc 
    sg <- R.getStdGen
    rs <- return $ take 256 $ R.randoms sg
    g <- initialize $ V.fromList rs
    l <- forM [2,4..n_parts] $ \np -> do 
        let w = mkWheel np inc
        sumA times w g 
    save_points n_parts l times
    print $ last l
