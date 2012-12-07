import qualified Data.IntMap as M
import Data.List (find, sortBy)
import System.Random.Mersenne as R

type Symbol = Int
type ProbS = [(Double, Symbol)]

data Tree = Branch Symbol Tree Tree
          | Root {leftRoot :: Tree, rightRoot :: Tree }
          | Node Symbol Double
          deriving (Show, Read)
 
sortProbs :: [(Double, Symbol)] -> [(Double, Symbol)]
sortProbs = sortBy (\(x,_) (y,_) -> compare x y)

binM p0 = sortProbs [(p0, 0), (1, 1)]

t = Root (Branch 1 (Branch 1 (Node 1 0.2) 
                             (Node 0 0.7))
                   (Node 0 0))
         (Branch 0 (Branch 1 (Node 1 0.6) 
                             (Node 0 0.7))
                   (Node 0 0))

t2 = Root (Branch 1 (Branch 1 (leftRoot t)
                              (Node 0 0.7))
                    (Node 0 0))
          (Branch 0 (Branch 1 (leftRoot t) 
                              (Node 0 0.7))
                    (rightRoot t))

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

randInit tree@(Root l r) g = do
    isLeft <- random g :: IO Bool
    if isLeft
      then ri [] l g
      else ri [] r g
    where
        ri seq (Node b p) g = return.reverse $ b:seq
        ri seq (Branch b l p) g = do
            isLeft <- random g
            if isLeft
              then ri (b:seq) l g
              else ri (b:seq) r g
 
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
                       
pl :: [(Double, Int)]
pl = [(0.7, 3), (0.85, 2), (1, 1)]

randW :: [(Double, Int)] -> MTGen -> IO Int
randW pl rg = do
    r <- random rg
    case find ((>= r).fst) pl of
        Nothing -> error "Nope"
        Just (p, x) -> return x
