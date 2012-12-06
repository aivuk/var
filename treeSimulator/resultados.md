Árvore 1
========

    t = Root (Branch 1 (Branch 1 (Node 1 $ binM 0.2 0.8)
                                 (Node 0 $ binM 0.7 0.3))
                       (Node 0 $ binM 0 1))
             (Branch 0 (Branch 1 (Node 1 $ binM 0.6 0.4)
                                 (Node 0 $ binM 0.7 0.3))
                       (Node 0 $ binM 0 1))
    
    P(1 | 111) = 0.8
    P(1 | 01)  = 1
    P(1 | 011) = 0.3 
    P(1 | 110) = 0.4
    P(1 | 010) = 0.3
    P(1 | 00)  = 1

Tamanho da sequência: 10.003
[Arquivo da sequência](seq1)

VLMC
-----

    > system.time(vlmc(dt2, cutoff=4))
       user  system elapsed 
      0.048   0.000   0.047 
    
    > vlmc.dt1 <- vlmc(dt1, cutoff=4)
    > draw.vlmc(vlmc.dt1)
    [x]-( 3183 6819| 10002)-F
     +--[0]-( 1200 1983| 3183) <24.60>-F
     |   +--[0]-( 0 1200| 1200) <567.86>-T
     |   `--[1]-( 1200 783| 1983) <210.79>-T
     `--[1]-( 1983 4836| 6819) <12.02>-F
         +--[0]-( 0 1983| 1983) <681.41>-T
         `--[1]-( 1983 2852| 4835) <156.38>-F
             +--[0]-( 1400 583| 1983) <354.43>-T
             `--[1]-( 582 2269| 2851) <273.58>-T
BIC
------

    L = 11
    [r] -> [ 0 1 ]
        [0] -> [ 0 1 ]
        [1] -> [ 0 1 ]
            [1] -> [ 0 1 ]

    ./bic.exe alfabeto d 0 0.5  0.21s user 0.00s system 98% cpu 0.214 total
 
CCSR
-------

Tempo: 0.006s 
[Resultados](CSSR)

![Grafo da
cadeia](https://github.com/aivuk/var/raw/master/treeSimulator/CSSR/dot.png "Grafo da cadeia")



