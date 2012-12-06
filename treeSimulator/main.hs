import qualified Data.IntMap as M
import Data.List (find)
import System.Random.Mersenne as R

type Symbol = Int
type ProbS = M.IntMap Double

data Tree = Branch Symbol Tree Tree
          | Root {leftRoot :: Tree, rightRoot :: Tree }
          | Node Symbol ProbS
          deriving (Show, Read)

binM p0 p1 = M.fromAscList [(0, p0), (1, p1)]

t = Root (Branch 1 (Branch 1 (Node 1 $ binM 0.2 0.8) 
                             (Node 0 $ binM 0.7 0.3))
                   (Node 0 $ binM 0 1))
         (Branch 0 (Branch 1 (Node 1 $ binM 0.6 0.4) 
                             (Node 0 $ binM 0.7 0.3))
                   (Node 0 $ binM 0 1))

t2 = Root (Branch 1 (Branch 1 (leftRoot t)
                              (Node 0 $ binM 0.7 0.3))
                    (Node 0 $ binM 0 1))
          (Branch 0 (Branch 1 (leftRoot t) 
                              (Node 0 $ binM 0.7 0.3))
                    (rightRoot t))
 
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
        walkTree (x:xs) (Node lx lp) (Node rx rp) | x == lx = randS rg lp
                                                  | x == rx = randS rg rp 
        walkTree (x:xs) (Node lx lp) (Branch rx rl rr) | x == lx = randS rg lp
                                                       | x == rx = walkTree xs rl rr
        walkTree (x:xs) (Branch lx ll lr) (Node rx rp) | x == rx = randS rg rp
                                                       | x == lx = walkTree xs ll lr
 
        randS rg p = do
                    r <- random rg :: IO Double
                    if r <= (p M.! 0) 
                       then return $ 0:seq
                       else return $ 1:seq
                       
pl :: [(Double, Int)]
pl = [(0.7, 3), (0.85, 2), (1, 1)]

randW :: [(Double, Int)] -> MTGen -> IO Int
randW pl rg = do
    r <- random rg
    case find ((>= r).fst) pl of
        Nothing -> error "Nope"
        Just (p, x) -> return x
