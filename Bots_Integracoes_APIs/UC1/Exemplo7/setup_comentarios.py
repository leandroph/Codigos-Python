import pandas as pd
import random

# Lista de frases típicas de e-commerce
frases = [
    "The product arrived late and the package was damaged.",
    "Excellent quality! I loved the color and the texture.",
    "Customer support was very helpful with my return.",
    "Not worth the price. It broke after two days.",
    "Shipping was super fast, arrived before the deadline.",
    "The manual is confusing and hard to understand.",
    "Five stars! Will definitely buy again.",
    "I'm disappointed with the battery life.",
    "Great value for money.",
    "The size is smaller than described on the website."
]

# Gera 50 comentários repetindo as frases aleatoriamente
dados = {
    "ID": range(1, 51),
    "Comentario_EN": [random.choice(frases) for _ in range(50)]
}

df = pd.DataFrame(dados)
df.to_csv("comentarios_en.csv", index=False)

print(" Arquivo 'comentarios_en.csv' gerado com sucesso!")