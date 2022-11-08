import numpy as np
from matplotlib import pyplot as plt

#PRIMEIRA QUESTÃO
#le o arquivo de dados passando como delimitador o espaço
#e o tipo de dados como float
file = np.loadtxt('dados.txt', dtype=float, delimiter=' ')

#usaremos um array numpy de forma a facilitar a plotagem dos graficos posteriormente
#e de forma a manter o nível de precisão
#aqui a variável files é definida como um array de arrays do numpy com tamanho fixo
#print(type(file))
#da forma que cada index do array é um array com dois pontos
#tal que file[i] = [x, f(x)]

#criamos arrays do numpy para os valores de x e de y dos dados
x = np.array([])
y = np.array([])

#criamos arrays do numpy para os valores após calcularmos as derivadas
x_final = np.array([])
y_final = np.array([])

#delta é a variação em x, de acordo com o pdf da atividade:
#delta = x[i+1] - x[i], sendo esse um valor constante.
#assim, podemos definir um delta com o segundo index do array
#em comparativo ao primeiro
#pegamos o x do index 1 e do index 0 do arquivo
delta = (file[1][0] - file[0][0])

#criamos uma função para o método da diferença avançada
def diferenca_avancada(y, y_posterior, delta):
    derivada = (y_posterior - y)/delta
    return derivada

#criamos uma função para o método da diferença atrasada
def diferenca_atrasada(y, y_anterior, delta):
    derivada = (y_anterior - y)/delta
    return derivada

#criamos uma função para o método da diferença centrada
def diferenca_centrada(y_anterior, y_posterior, delta):
    derivada = (y_posterior - y_anterior)/delta
    return derivada

#criamos uma variável de index que vai percorrer o array do arquivo
i = 0
#criamos uma variável para a quantidade de linhas e outra para a quantidade de colunas do arquivo
lin, col = file.shape

#agora cria-se um laço que percorre o array do arquivo e aplica os métodos
#da diferença avançada ao primeiro item
#da diferença atrasada ao ultimo
#e da diferença centrada ao restante
while i <= lin - 1:
    x = np.append(x, file[i][0])
    y = np.append(y, file[i][1])

    #pega o valor (x,y) inicial do arquivo e aplica diferença avançada
    if i == 0:
        x_final = np.append(x_final, file[i][0])
        y_final = np.append(y_final, diferenca_avancada(file[i][1], file[i+1][1], delta))

    #pega o valor (x,y) final do arquivo e aplica diferença atrasada
    elif i == lin - 1:
        x_final = np.append(x_final, file[i][0])
        y_final = np.append(y_final, diferenca_atrasada(file[i][1], file[i-1][1], delta))
    
    #aplica a diferença centrada ao restante
    elif i != lin - 1 and i != 0:
        x_final = np.append(x_final, file[i][0])
        y_final = np.append(y_final, diferenca_centrada(file[i-1][1], file[i+1][1], delta))

    i += 1

#para plotar os gráficos usamos o matplotlib
#e definimos primeiro o gráfico para comparar os dados do arquivo e os obtidos
plt.title("Comparação de dados") 
plt.xlabel("eixo x") 
plt.ylabel("eixo y")
plt.plot(x,y) 
plt.plot(x_final,y_final) 
plt.legend(['Dados do arquivo','Dados resultantes'], fontsize=12)
plt.show()

#para finalizar criamos o arquivo que vai receber os dados gerados
arquivo = open("derivada.txt", "a")

#interamos nos arrays existentes para adicionar as informações ao arquivo
j = 0
while j <= lin - 1:
    arquivo.write(f"{x_final[j]} {y_final[j]} \n")
    j += 1

#fechamos o arquivo
arquivo.close()

#SEGUNDA QUESTÃO
#inicialmente, precisamos definir a função que vai retornar o valor desejado pelo método
#de lagrange, que tem a forma Pn(x) = L0f(x0) + L1f(x1) + ... + Lnf(xn)
#essa função irá retornar o valor do resultado que se deseja saber ou seja x = 26
def polinomio_lagrange(x, x_valores, y_valores):
    #pega a quantidade de f(x) disponíveis e cria um array que armazenará cada um dos coeficientes encontrados
    lin = len(y_valores)
    coeficientes = []
    i = 0
    #agora iteramos inicialmente nos indicies "maiores"
    for i in range(lin):
        l = 1
        #e depois nos menores, de forma a criar:
        for j in range(lin):
             if j != i:
                #o coeficiente terá a forma: Ln = ((x - x0)/(xn - x0)) * ((x - x1)/(x2 - x1)) ... ((x - xn-1)/(xn - xn-1))
                l *= (x - x_valores[j])/(x_valores[i] - x_valores[j])
        #adicionamos ao arrai cada coeficiente gerado após percorrer o array
        coeficientes.append(l)
    #e instanciamos o polinomio
    polinomio = 0
    k = 0
    coef_lin = len(coeficientes)

    #conferimos se temos a mesma quantidade de coeficientes e valores de y
    if coef_lin == lin:
        #e criamos o polinomio com o valor desejado
        for k in range(coef_lin):
            polinomio += coeficientes[k]*y_valores[k]

    return polinomio 

#agora criamos nosso array de dados
x_valores = [12, 22, 30, 38, 46]
y_valores = [320, 490, 540, 500, 480]

#e chamamos a função pro valor que queremos descobrir
resultado = polinomio_lagrange(26, x_valores, y_valores)
print(resultado)