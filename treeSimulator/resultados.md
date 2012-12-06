Sumários dos resultados
=======================

 * [Árvore 1](#Árvore-1)

<table>
    <thead>
        <th> Algoritmo</th>
        <th> Tempo</th>
        <th> Parâmetros</th>
        <th>Tamanho da seq.</th>
    </thead>
    <tbody>
         <tr>
             <td>VLMC</td>
             <td> 0.048</td> 
             <td> cutoff=4</td> 
             <td>10003</td>
         </tr>
         <tr>
             <td>BIC</td>
             <td> 0.5</td> 
             <td> c=0,5</td> 
             <td>10003</td>
         </tr>
         <tr>
             <td>CSSR</td>
             <td> 0.001</td> 
             <td> Mem. máxima=4</td> 
             <td>10003</td>
         </tr>
 
    </tbody>
</table>

 * [Árvore 2](#Árvore-2) 

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

### Resultados

 * [VLMC](#vlmc)
 * [BIC](#bic)
 * [CSSR](#cssr)

VLMC
-----

### Tempo de execução

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

c = 0.5

    L = 11
    [r] -> [ 0 1 ]
        [0] -> [ 0 1 ]
        [1] -> [ 0 1 ]
            [1] -> [ 0 1 ]

    ./bic.exe alfabeto d 0 0.5  0.21s user 0.00s system 98% cpu 0.214 total
 
CSSR
-------

Tempo: 0.006s 
[Resultados](CSSR)

![Grafo da
cadeia](https://github.com/aivuk/var/raw/master/treeSimulator/CSSR/dot.png "Grafo da cadeia")

Árvore 2
========

    t2 = Root (Branch 1 (Branch 1 (leftRoot t)
                                  (Node 0 $ binM 0.7 0.3))
                        (Node 0 $ binM 0 1))
              (Branch 0 (Branch 1 (leftRoot t)
                                  (Node 0 $ binM 0.7 0.3))
                        (rightRoot t))

Tamanho da sequência: 10.003
[Arquivo da sequência](seq2)

### Resultados

 * [VLMC](#vlmc-1)
 * [BIC](#bic-1)
 * [CSSR](#cssr-1)

VLMC
-----

### Tempo de execução

    > system.time(vlmc(dt, cutoff=5))
       user  system elapsed 
      0.056   0.000   0.056 

    > draw(vlmc.dt)
    [x]-( 2599 7403| 10002)-F
     +--[0]-( 236 2363| 2599) <237.95>-F
     |   +--[0]-( 84 152| 236) <62.34>-F
     |   |   +--[0]-( 0 84| 84) <36.96>-T
     |   |   `--[1]-( 84 68| 152) <12.18>-T
     |   `--[1]-( 152 2211| 2363) <11.07>
     |       `--[1]-( 152 2210| 2362) <0.00>-F
     |           +--[0]-( 0 1600| 1600) <106.43>-T
     |           `--[1]-( 152 610| 762) <76.82>
     |               `--[1]-( 152 610| 762) <0.00>
     |                   `--[0]-( 102 422| 524) <0.04>
     |                       `--[1]-( 98 399| 497) <0.01>
     |                           `--[1]-( 98 398| 496) <0.00>
     |                               `--[1]-( 21 109| 130) <0.56>
     |                                   `--[1]-( 21 109| 130) <0.00>
     |                                       `--[0]-( 15 70| 85) <0.07>
     |                                           `--[0]-( 3 0| 3) <5.20>-T
     `--[1]-( 2363 5040| 7403) <64.84>-F
         +--[0]-( 0 2363| 2363) <908.52>-T
         `--[1]-( 2362 2677| 5039) <243.63>-F
             +--[0]-( 1600 763| 2363) <208.52>-T
             `--[1]-( 762 1914| 2676) <189.39>-F
                 +--[0]-( 0 762| 762) <255.37>-T
                 `--[1]-( 762 1152| 1914) <56.57>-F
                     +--[0]-( 524 238| 762) <130.27>-T
                     `--[1]-( 238 914| 1152) <96.39>-T


BIC
------

c=0.5
Tempo=0.16s

    L = 11
    [r] -> [ 0 1 ]
        [0] -> [ 0 1 ]
            [0] -> [ 0 1 ]
            [1] -> [ 1 ]
                [1] -> [ 0 1 ]
        [1] -> [ 0 1 ]
            [1] -> [ 0 1 ]
                [1] -> [ 0 1 ]
                    [1] -> [ 0 1 ]
    
    ./bic.exe alfabeto ../var/treeSimulator/seq2.fast 0 0.2  0.16s user 0.00s system 97% cpu 0.160 total
 
CSSR
-------

Tempo: 0.01s 

Memória máxima: 10

[Resultados](CSSR/seq2)

 
