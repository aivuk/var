import qualified Data.IntMap as M
import Data.List (find, sortBy)
import System.Random.Mersenne as R
import Control.Monad (forM_)

type Symbol = Int
type ProbS = [(Double, Symbol)]

data Tree = Branch Symbol Tree Tree
          | Root {leftRoot :: Tree, rightRoot :: Tree }
          | Node Symbol Double
          deriving (Show, Read)
 
randTree max_depth g = do
    left <- rt max_depth 0 g
    right <- rt max_depth 1 g
    return $ Root left right
         where
            rt 0 b g = return.(Node b) =<< random g 
            rt md b g = do
                isBranch <- random g :: IO Bool
                if isBranch
                  then do 
                    l <- rt (md - 1) 0 g
                    r <- rt (md - 1) 1 g                 
                    return $ Branch b l r
                  else do 
                    return.(Node b) =<< random g

genSeq :: MTGen -> Int -> Tree -> [Int] -> IO [Int]
genSeq rg size tree initSeq = gs size initSeq
    where
        gs size seq | size == 0 = return seq
                    | otherwise = do
                        new_seq <- newSymbol rg tree seq 
                        gs (size - 1) new_seq

newSymbol rg (Root t1 t2) seq = walkTree seq t1 t2
    where
        walkTree (x:xs) (Branch lx ll lr) (Branch rx rl rr) | x == lx = walkTree xs ll lr
                                                            | x == rx  = walkTree xs rl rr
        walkTree (x:xs) (Node lx lp) (Node rx rp) | x == lx = randS lp rg 
                                                  | x == rx = randS rp rg 
        walkTree (x:xs) (Node lx lp) (Branch rx rl rr) | x == lx = randS lp rg
                                                       | x == rx = walkTree xs rl rr
        walkTree (x:xs) (Branch lx ll lr) (Node rx rp) | x == rx = randS rp rg
                                                       | x == lx = walkTree xs ll lr
 
        randS p rg = do
                    r <- random rg :: IO Double
                    if r <= p 
                       then return $ 0:seq
                       else return $ 1:seq
                       
main = do
    g <- getStdGen
    forM_ [100, 1000, 10000, 100000, 1000000] $ \steps -> do
        forM_ [10, 20..100] $ \treeDepth -> do
           forM_ [1..10] $ \i -> do
               randomTree <- randTree treeDepth g
               randInit <- return.(map (\x -> if x then 1 else 0)).(take (100)) =<< randoms g
               dataSeq <- genSeq g steps randomTree randInit 
               let treeFile = "tree-" ++ (show treeDepth) ++ "-" ++ (show i) ++ "-" ++ (show steps) 
               writeFile treeFile (show randomTree)
               writeFile (treeFile ++ ".data") (show dataSeq)
