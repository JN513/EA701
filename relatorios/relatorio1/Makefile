# Nome do arquivo principal sem extensão
MAIN = relatorio1
# Nome do PDF final
OUT = Aula3_Yoshida_Avelar

# Compilador LaTeX
LATEX = pdflatex
LATEXFLAGS = -interaction=nonstopmode -halt-on-error -output-directory=build -jobname=$(OUT)

# Regra padrão
all: build $(OUT).pdf

# Compila o relatório
$(OUT).pdf: $(MAIN).tex
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	# Move o PDF gerado para a raiz do projeto
	mv build/$(OUT).pdf .

# Cria diretório build se não existir
build:
	mkdir -p build

# Limpa arquivos auxiliares (mantém o PDF)
clean:
	rm -rf build/*
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk

# Limpa tudo (inclusive o PDF final)
distclean: clean
	rm -f $(OUT).pdf
