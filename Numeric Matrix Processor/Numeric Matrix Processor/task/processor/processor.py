class MatrixOperations:
    """ This class perform matrix operations """
    def __init__(self):
        self.menu()

    def menu(self):
        operations = {
            "0": self.exit,
            "1": self.add_matrices,
            "2": self.multiply_constant,
            "3": self.multiply_matrices,
            "4": self.transpose_matrix,
            "5": self.determinant,
            "6": self.inverse_matrix
        }
        print("1. Add matrices\n"
              "2. Multiply matrix by a constant\n"
              "3. Multiply matrices\n"
              "4. Transpose matrix\n"
              "5. Calculate a determinant\n"
              "6. Inverse matrix\n"
              "0. Exit\n")
        choice = input('Your choice: ')
        if operations.get(choice, False):
            operations[choice]()
        else:
            print('ERROR')
            self.menu()

    def add_matrices(self):
        try:
            dim1 = input('Enter size of first matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            dim2 = input('Enter size of second matrix: ').split(' ')
            assert len(dim2) == 2, "Wrong matrix dimension"
            r2, c2 = [int(d) for d in dim2]
            mat2 = self.read_matrix(r2, c2)
            assert r1 == r2 and c1 == c2, "The operation cannot be performed."
            result = []
            for i in range(int(r1)):
                row = []
                for j in range(int(c1)):
                    row.append(str(mat1[i][j] + mat2[i][j]))
                result.append(row)
            print('The result is: ')
            for row in result:
                print(' '.join(row))
            print('')
            return self.menu()
        except AssertionError as e:
            print(e, ' Try again.')
            self.menu()

    def multiply_constant(self):
        try:
            dim1 = input('Enter size of matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            const = float(input('Enter constant: '))
            result = []
            for i in range(r1):
                row = []
                for j in range(c1):
                    row.append(str(mat1[i][j] * const))
                result.append(row)
            print('The result is: ')
            for row in result:
                print(' '.join(row))
            print('')
            return self.menu()
        except (ValueError, AssertionError) as e:
            print(e, 'Try again.')
            self.menu()

    def multiply_matrices(self):
        try:
            dim1 = input('Enter size of first matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            dim2 = input('Enter size of second matrix: ').split(' ')
            assert len(dim2) == 2, "Wrong matrix dimension"
            r2, c2 = [int(d) for d in dim2]
            mat2 = self.read_matrix(r2, c2)
            assert c1 == r2, "The operation cannot be performed."
            result = []
            for i in range(r1):
                row = []
                for j in range(c2):
                    a1 = mat1[i][:c1]
                    a2 = [el[j] for el in mat2]
                    row.append(str(sum([x*y for x, y in zip(a1, a2)])))
                result.append(row)
            print('The result is: ')
            for row in result:
                print(' '.join(row))
            print('')
            return self.menu()
        except AssertionError as e:
            print(e, '')

    @staticmethod
    def exit():
        exit('')

    def read_matrix(self, n_rows=None, n_cols=None):
        matrix = []
        for _ in range(n_rows):
            row = [*map(float, input().split(' '))]
            if len(row) != n_cols:
                print('Wrong number of columns.Try again.')
                return self.read_matrix(n_rows, n_cols)
            matrix.append(row)
        return matrix

    def transpose_matrix(self):
        transposition = {
            "1": self.main_diagonal_transposition,
            "2": self.side_diagonal_transposition,
            "3": self.v_transposition,
            "4": self.h_transposition
        }
        print("1. Main diagonal\n"
              "2. Side diagonal\n"
              "3. Vertical line\n"
              "4. Horizontal line")
        choice = input('Your choice: ')

        if not transposition.get(choice, False):
            print('ERROR')
            return self.menu()
        try:
            dim1 = input('Enter size of matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            result = transposition[choice](mat1, r1, c1)
            print('The result is: ')
            for row in result:
                print(' '.join([*map(str, row)]))
            print('')
        except AssertionError as e:
            print(e, "Try again.")
            return self.menu()

    def calc_determinant(self, matrix, dimension):
        if len(matrix) == 1 and len(matrix[0]) == 1:
            return matrix[0][0]
        elif len(matrix) == 2 and len(matrix[0]) == 2:
            return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
        else:
            cofactor_list = self.calc_cofactor_list(matrix, dimension)
            return sum(cofactor_list)

    def calc_cofactor_list(self, matrix, dimension, row_number=0, inverse=False):
        det_list = []
        temp_row = matrix.pop(row_number)
        for i in range(dimension[1]):
            new_sub_matrix = [[el for n, el in enumerate(row) if n != i] for row in matrix]
            complement = temp_row[i] * (-1) ** (i + row_number + 2) if not inverse else (-1) ** (i + row_number + 2)
            det_sub_matrix = self.calc_determinant(new_sub_matrix, (dimension[0] - 1, dimension[1] - 1))
            det_list.append(complement * det_sub_matrix)
        matrix.insert(row_number, temp_row)
        return det_list

    def determinant(self):
        try:
            dim1 = input('Enter size of matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            assert r1 == c1, "The matrix must be a square matrix"
            determinant = self.calc_determinant(mat1, dimension=(r1, c1))
            print('The result is:')
            print(determinant)
            print('\n')
            return self.menu()
        except AssertionError as e:
            print(e, ' Try again.')
            return self.menu()

    def inverse_matrix(self):
        try:
            dim1 = input('Enter size of matrix: ').split(' ')
            assert len(dim1) == 2, "Wrong matrix dimension"
            r1, c1 = [int(d) for d in dim1]
            mat1 = self.read_matrix(r1, c1)
            assert r1 == c1, "The matrix must be a square matrix"
            matrix_determinant = self.calc_determinant(mat1, (r1, r1))
            assert matrix_determinant != 0.0, "This matrix doesn't have an inverse."
            cofactor_matrix = self.calc_inverse_matrix(mat1, (r1, r1))
            transposed_inverse_matrix = self.main_diagonal_transposition(cofactor_matrix, rows=r1, cols=c1)
            inverse_matrix = [[*map(lambda x: x / matrix_determinant, row)] for row in transposed_inverse_matrix]
            print('The result is:')
            for row in inverse_matrix:
                print(' '.join([*map(str, row)]))
            print('\n')
            return self.menu()
        except AssertionError as e:
            print(e)
            return self.menu()

    def calc_inverse_matrix(self, matrix, dimension):
        cofactor_matrix = []
        for n, row in enumerate(matrix):
            cofactor_matrix.append(self.calc_cofactor_list(matrix, dimension, n, inverse=True))
        return cofactor_matrix

    @staticmethod
    def h_transposition(matrix, rows, cols):
        return [el for el in matrix[::-1]]

    @staticmethod
    def v_transposition(matrix, rows, cols):
        return [el[::-1] for el in matrix]

    @staticmethod
    def main_diagonal_transposition(matrix, rows, cols):
        output = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(matrix[j][i])
            output.append(row)
        return output

    @staticmethod
    def side_diagonal_transposition(matrix, rows, cols):
        output = []
        for i in range(1, rows + 1):
            row = []
            for j in range(1, cols + 1):
                row.append(matrix[-j][-i])
            output.append(row)
        return output


if __name__ == "__main__":
    MatrixOperations()
