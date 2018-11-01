MaqLavM = readfis('MaqLavMoM');
MaqLavC = readfis('MaqLavCentroid');
MaqLavSugMin = readfis('MaqLavSugMin');
MaqLavSugPro = readfis('MaqLavSugProd');

lin = 1;

for (i=0:10:100),
    for (j=0:10:100),
        entrada(lin,:) = [i,j];
        lin = lin + 1;
    end
end

saida = evalfis(entrada, MaqLavM)
output = [entrada saida]
csvwrite('outputMoM.csv', output)

saida = evalfis(entrada, MaqLavC)
output = [entrada saida]
csvwrite('outputCentroid.csv', output)

saida = evalfis(entrada, MaqLavSugMin)
output = [entrada saida]
csvwrite('outputSugMin.csv', output)

saida = evalfis(entrada, MaqLavSugPro)
output = [entrada saida]
csvwrite('outputSugProd.csv', output)
