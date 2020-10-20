# from app import App

# app = App()
# app.start_app()

from classes import Matrix

aux = list(range(65))
matrix = Matrix(8, 8)
matrix.list_to_matrix(aux)

result = list(map(lambda x: x.matrix, matrix.return_submatrix_by_size(4, 4)))

for r in result:
    print(r)
print(len(result))
