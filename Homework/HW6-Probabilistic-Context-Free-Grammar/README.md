# HW6-Probabilistic Context Free Grammar

#### Run
```
$ cd CMP462\ HW06\ Data
$ java -jar pcfg.jar parse -t dev.sen *.gr
```

#### Result
Result for sentence 1-4
```
[PCFGParser]    log prob = -27.54   sentence : Arthur is the king .
[PCFGParser]    best parse tree:
(START
   (S1
      (NV
         (NP
            (NNP Arthur))
         (VP
            (VBZ is)
            (NP
               (DT the)
               (Nbar
                  (NN king))))) .))
[PCFGParser]    log prob = -47.55   sentence : Arthur rides the horse near the castle .
[PCFGParser]    best parse tree:
(START
   (S1
      (NV
         (NP
            (NNP Arthur))
         (VP
            (VBZ rides)
            (NP
               (DT the)
               (Nbar
                  (Nbar
                     (NN horse))
                  (PP
                     (IN near)
                     (NP
                        (DT the)
                        (Nbar
                           (NN castle)))))))) .))
[PCFGParser]    log prob = -25.10   sentence : riding to Camelot is hard .
[PCFGParser]    best parse tree:
(START
   (S1
      (NV
         (NP
            (@VBG-TO
               (VBG riding)
               (TO to))
            (Nbar
               (NNP Camelot)))
         (VP
            (VBZ is)
            (JJ hard))) .))
[PCFGParser]    log prob = -22.48   sentence : do coconuts speak ?
[PCFGParser]    best parse tree:
(START
   (S1
      (QA
         (VB do)
         (NV
            (NP
               (Nbar
                  (NNS coconuts)))
            (VP
               (VB speak)))) ?))
```