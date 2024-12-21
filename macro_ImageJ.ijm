// Definir o diretório onde as imagens estão localizadas
dir = "C:\\Users\\caiod\\OneDrive\\Documentos\\Projetos Python\\IC\\Imagens Finais\\Resultados GEM-Laser\\";
list = getFileList(dir);

// Definir a escala (exemplo: 1 pixel = 5.25 micrômetros) 
pixelWidth = 5.25021; 
pixelHeight = 5.25021;
unit = "microns";  // A unidade física

// Excluir o arquivo de resumo se já existir
summaryFile = dir + "summary_stddev.csv";
if (File.exists(summaryFile)) {
    File.delete(summaryFile);
}

// Cabeçalho do arquivo de resumo
File.append("Imagens,Desvio Padrao Area,Desvio Padrao Circularidade", summaryFile);

// Função para calcular desvio padrão
function stdDev(arr) {
    mean = 0;
    sum = 0;
    for (i = 0; i < arr.length; i++) {
        mean += arr[i];
    }
    mean /= arr.length;
    for (i = 0; i < arr.length; i++) {
        sum += pow(arr[i] - mean, 2);
    }
    return sqrt(sum / (arr.length - 1));
}

// Iterar sobre todas as imagens na pasta
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".jpg") || endsWith(list[i], ".png")) { 
        open(dir + list[i]);  // Abrir a imagem

        // Definir a escala da imagem
        run("Set Scale...", "distance=1 known=" + pixelWidth + " pixel=1 unit=" + unit);

        // Converter a imagem para escala de cinza
        run("8-bit");

        // Aplicar FFT Bandpass Filter
        run("Bandpass Filter...", "filter_large=40 filter_small=3 suppress=None tolerance=5");

        // Definir manualmente os valores de threshold usando o método Li
        setAutoThreshold("Li");
        run("Threshold...");

        // Converter para máscara
        run("Convert to Mask");

        // Limpar tabela de resultados anterior
        run("Clear Results");

        // Analisar partículas, habilitar circularidade, e salvar dados
        run("Analyze Particles...", "size=4500-8000 circularity=0.00-1.00 display exclude clear include summarize");

        // Arrays para armazenar os valores de área e circularidade
        areas = newArray(nResults());
        circularidades = newArray(nResults());

        // Coletar os dados de área e circularidade
        for (j = 0; j < nResults(); j++) {
            areas[j] = getResult("Area", j);
            circularidades[j] = getResult("Circ.", j);  // Coletar a circularidade corretamente
        }

        // Calcular o desvio padrão da área e da circularidade
        stdDevArea = stdDev(areas);
        stdDevCirc = stdDev(circularidades);

        // Salvar os resultados no arquivo de resumo
        File.append(list[i] + "," + stdDevArea + "," + stdDevCirc, summaryFile);

        // Fechar a imagem processada
        close();
    }
}

// Salvar o arquivo Summary com todas as imagens
IJ.renameResults("Summary", "Results");
summaryCsv = dir + "summary.csv";
saveAs("Results", summaryCsv);
