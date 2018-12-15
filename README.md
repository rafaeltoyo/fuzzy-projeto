# fuzzy-projeto
Biblioteca em Python para se trabalhar com Sistemas Fuzzy.

Esse código foi desenvolvido para a disciplina "CSI56 - Sistemas Fuzzy" da Universidade Tecnológia Federal do Paraná no segundo semestre de 2018.

> Vale notar que a estrutura dos scripts não está na melhor forma possível, porém é funcional. O autor não possui experiência suficiente na linguagem Python e há uma grande despadronização do código construído devido ao processo de aprendizagem da linguagem junto a realização da matéria.

# Diretórios

## dataset
Apenas arquivos gerados para testes.

## exercicios
Códigos fazendo uso da biblioteca para atender requisitos das etapas de entregas da disciplina.

## fuzzychan
Código fonte da biblioteca. Sua estrutura interna será melhor discutida a seguir.

## genetic
Implementação própria de um Algoritmo Genético para integrar à biblioteca fuzzychan.

## old
Códigos antigos não mais utilizados, mas guardados para consulta para readequação na biblioteca fuzzychan.

## pp3-teste 
Arquivos gerados no MatLab para comparar com resultados gerados pela biblioteca para validar seu funcinamento.

# Código fonte (fuzzychan)
No diretório raiz há arquivos com implementações gerais que fazem uso de todos submódulos.

## classifier
Implementação de modelos para classificação de dados a partir de Conjuntos Fuzzy.
> Apenas foi realizado o método de Wang Mendel

## continuous
Implementação dos conjuntos de forma a simular comportamento contínuo (sem gerar dados em memória).
> Não foi terminado todas implementações objetivadas inicialmente, porém há implementações de forma discreta para utilizá-las.

## inference
Implementação de modelos para sistemas de inferência Fuzzy.
> Foram implementados os modelos Mamdani e Takagi-Sugeno.

## v1
Código depreciado devido a modificações nos arquivos bases, porém funcional e utilizado nas primeiras entregas no projeto. Semelhante ao diretório old, é mantido a fins de consulta, porém esses códigos contidos nesse diretório ainda são utilizados nos entregáveis do diretório exercicios.
