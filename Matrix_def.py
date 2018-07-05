from numpy import *
import numpy as np
import warnings
import tensorflow as tf
import re

'''
    py_matrix_to_str(matrix) - converts matrix to string (in native python)
    str_to_py_matrix(str) - python matrix to string (native python)
    np_matrix_to_str(matrix) - numpy matrix to string
    str_to_np_matrix(str)- str to numpy matrix
    tensor_to_str(tensor) - TensorFlow tensor to string
    str_to_tensor(str) - string to tensor

    (: (:
'''


def digit_float_str(str):
    try:
        final = int(str)
    except ValueError:
        try:
            final = float(str)
        except ValueError:
            return final
    return final


def py_matrix_to_str(matrix):
    # Check if is a vector
    term = False
    for item in matrix:
        term = not isinstance(item, list)
        if not term:
            break
    if term:
        return ','.join(map(str, matrix))

    # Check if matrix is valid
    in_type = str(type(matrix))
    if not isinstance(matrix, list):
        raise TypeError('Expecting valid python matrix - Got ' + in_type + ' instead')
    temp = -1
    for row in matrix:
        if not isinstance(row, list):
            raise Exception('py_matrix_to_string - Not a valid matrix')
        curr = len(row)
        if (temp == -1):
            temp = curr
        if (temp != curr):
            raise Exception('py_matrix_to_string - Python matrix not valid - Was expecting an n x m matrix')

    # Convert matrix to string
    col_delim = ' '
    row_delim = ';'
    if isinstance(matrix[0][0], float):
        return "PYTHON_" + row_delim.join(col_delim.join('%0.5f' % x for x in y) for y in matrix)
    if isinstance(matrix[0][0], int):
        return "PYTHON_" + row_delim.join(col_delim.join('%0.0f' % x for x in y) for y in matrix)
    if isinstance(matrix[0][0], str):
        return "PYTHON_" + row_delim.join(col_delim.join(x for x in y) for y in matrix)
    else:
        return "PYTHON_" + row_delim.join(col_delim.join(x for x in y) for y in matrix)


def str_to_py_matrix(input_string):
    if input_string[:6] == "PYTHON":
        matrix = str_to_np_matrix(input_string)
        return matrix
    else:
        return "String is not from a 2D list matrix string"


def np_matrix_to_str(matrix):
    col_delim = ' '
    row_delim = ';'
    if not isinstance(matrix, ndarray):
        raise Exception('Was Expecting a numpy array as input - Got a ' + str(type(matrix)) + ' instead')
    try:
        if matrix.ndim == 1:
            return col_delim.join(x for x in matrix)
        for (x, y), value in np.ndenumerate(matrix):
            if isinstance(matrix[x, y], basestring):
                matrix[x, y] = matrix[x, y].replace(' ', '##')
        if matrix.ndim == 2:
            type = np.array(matrix)
            type = str(type.dtype)
            if 'float' in type:
                matrix = row_delim.join(col_delim.join('%0.5f' % x for x in y) for y in matrix)
                matrix = matrix.replace("; ;", " ")
                matrix = matrix.replace(";;;", ";")
                return "NUMPY_" + matrix.replace(";.;", ".")
            if 'int' in type:
                matrix = row_delim.join(col_delim.join('%0.0f' % x for x in y) for y in matrix)
                matrix = matrix.replace("; ;", " ")
                return "NUMPY_" + matrix
            if 'str' in type:
                matrix = row_delim.join(col_delim.join(x for x in y) for y in matrix)
                matrix = matrix.replace("; ;", " ")
                matrix = matrix.replace(";;;", ";")
                return "NUMPY_" + matrix
            else:
                return "NUMPY_" + row_delim.join(col_delim.join(x for x in y) for y in matrix)
        else:
            raise Exception('Was expecting a numpy matrix. Got a ' + str(matrix.ndim) + 'D numpy instead')
    except TypeError:
        raise Exception('Input matrix is not valid')


def str_to_np_matrix(input_str):
    input_str = input_str.split('_')
    input_str = input_str[1]
    if not isinstance(input_str, basestring):
        raise Exception("Was exprecting str but got " + str(type(input_str)) + " instead")
    try:
        matrix = np.matrix(input_str)
    except NameError:
        input_str = input_str.replace(';', '"],["')
        input_str = input_str.replace(' ', '","')
        input_str = '[["' + input_str + '"]]'
        input_str = input_str.replace('##', ' ')
        input_str = input_str.replace('[,', '[')
        matrix = np.matrix(eval(input_str))
        for (x, y), value in np.ndenumerate(matrix):
            if matrix[x, y].isdigit():
                matrix[x, y] = int(matrix[x, y])
    except TypeError:
        input_str = input_str.replace(';', '"],["')
        input_str = input_str.replace(' ', '","')
        input_str = '[["' + input_str + '"]]'
        matrix = np.matrix(eval(input_str))
        for (x, y), value in np.ndenumerate(matrix):
            if matrix[x, y].isdigit():
                matrix[x, y] = int(matrix[x, y])
    return matrix


def tensor_to_str(tensor):
    session = tf.Session()
    str_tensor = str(session.run(tensor))
    str_tensor = str_tensor.replace('\n', ',')
    pattern = re.compile(r'(,){2,}')
    pattern_s = re.compile(r'(\s){2,}')
    str_tensor = re.sub(pattern_s, ',', str_tensor)
    str_tensor = re.sub(' ', ',', str_tensor)
    str_tensor = re.sub(pattern, ',', str_tensor)
    str_tensor = re.sub(r"(?!(([^']*'){2})*[^']*$),", " ", str_tensor)
    str_tensor = str_tensor.replace("[,", '[')
    type = tf.Variable(tensor)
    type = str(type.dtype)
    type = re.search("'(.*)'", type)
    str_tensor = str_tensor + "_" + type.group(1) + "_tensor"
    session.close()
    return str_tensor


def str_to_tensor(str_tensor):
    str_tensor = str_tensor.split('_')
    np_array = np.array(eval(str_tensor[0]))
    type = str_tensor[1]
    if str_tensor[3] != "tensor":
        raise Exception("String is not a tensor")
    tensor = tf.convert_to_tensor(np_array)
    tensor = tf.cast(tensor, eval(type))
    return tensor

'''
if __name__ == '__main__':
    # matrix test
    print '---------- Matrix ----------'
    print '----------------------------\n\n'
    print 'TEST CASE #1'
    a = [[8.0, 7.5, 8, 90, 95],
         [7.5, 8.0, 7.5, 8.5, 1.00],
         [8.0, 8.0, 8.0, 9.0, 9.5]]

    print "Input(float): " + str(a)

    string_a = py_matrix_to_str(a)

    print '----------'

    print "String: " + string_a
    print '----------'

    b = str_to_py_matrix(string_a)

    print "Back to matrix: " + str(b)
    print '----------'
    print 'TEST CASE #2'
    a = [[8, 7, 8, 9, 9],
         [7, 8, 7, 8, 1],
         [8, 8, 8, 9, 9.]]

    print "Input(int): " + str(a)

    string_a = py_matrix_to_str(a)

    print '----------'

    print "String: " + string_a
    print '----------'

    b = str_to_py_matrix(string_a)

    print "Back to matrix: " + str(b)

    print '\n\n---------- Numpy Matrix Testing ----------'
    print '------------------------------------------\n\n'
    print 'TEST CASE #1'
    a = np.asarray([[1, 1, 2, 3, 4],  # 1st row
                    [2, 6, 7, 8, 9],  # 2nd row
                    [3, 6, 7, 8, 9],  # 3rd row
                    [4, 6, 7, 8, 9],  # 4th row
                    [5, 6, 7, 8, 9]  # 5th row
                    ], dtype=int64)
    print '----------'
    print 'Input(int) : \n' + str(a)
    str_a = np_matrix_to_str(a)
    print '----------'
    print 'Generated string: ' + str_a
    print '----------'
    b = str_to_np_matrix(str_a)
    print 'Back to numpy: \n' + str(b)
    print '----------'
    print 'TEST CASE #2'
    a = np.asarray([[1.0,2.0,2.31, 3.90, 4.1],  # 1st row
                    [2.123, 6.6, 7.7, 8.8, 9.1],  # 2nd row
                    [3.1, 6.81, 7.7, 8.9, 9.1],  # 3rd row
                    [4.1, 6.2, 7.2, 8.8, 9.1],  # 4th row
                    [5.1, 6.2, 7.9, 8.7, 9.8]  # 5th row
                    ])
    print '----------'
    print 'Input(float) : \n' + str(a)
    str_a = np_matrix_to_str(a)
    print '----------'
    print 'Generated string: ' + str_a
    print '----------'
    b = str_to_np_matrix(str_a)
    print 'Back to numpy: \n' + str(b)

    a = np.asarray([  # 1st row
                    [2.0, 6.0, 7.9, 8.8, 9.9],  # 2nd row
                    [3.8, 6.6, 7.8, 8.8, 9.8],  # 3rd row
                    [4, 6, 7.6, 8.7, 9.7],  # 4th row
                    [5, 6, 7, 8, 9]  # 5th row
                    ], dtype=float64)
    print '----------'
    print 'Input(float) : \n' + str(a)
    str_a = np_matrix_to_str(a)
    print '----------'
    print 'Generated string: ' + str_a
    print '----------'
    b = str_to_np_matrix(str_a)
    print 'Back to numpy: \n' + str(b)

    print '\n\n---------- Tensor Testing----------'
    print '-----------------------------------\n\n'
    sess = tf.Session()
    print 'TEST CASE #1'
    print '----------'
    b = tf.constant(np.arange(13, 25, dtype=np.int32),
                    shape=[2, 3, 2])

    print 'Input(int32): ' + str(b)
    print '----------'
    a = tensor_to_str(b)
    print 'String: \n' + a

    c = str_to_tensor(a)
    print '----------'
    print 'Tensor from String: \n' + str(sess.run(c))
    print 'Generated Tensor info: ' + str(c)
    print '----------'
    print 'TEST CASE #2'
    print '----------'
    b = tf.constant(np.arange(13.25, 20.5, dtype=np.float32),
                    shape=[3, 3, 2])

    print 'Input(float32): ' + str(b)
    print '----------'
    a = tensor_to_str(b)
    print 'String: \n' + a

    c = str_to_tensor(a)
    print '----------'
    print 'Tensor from String: \n' + str(sess.run(c))
    print 'Generated Tensor info: ' + str(c)
    print '----------'
    print 'TEST CASE #3'
    print '----------'
    b = tf.constant(np.arange(13, 25, dtype=np.int64),
                    shape=[2, 3, 2])

    print 'Input(int64): ' + str(b)
    print '----------'
    a = tensor_to_str(b)
    print 'String: \n' + a

    c = str_to_tensor(a)
    print '----------'
    print 'Tensor from String: \n' + str(sess.run(c))
    print 'Generated Tensor info: ' + str(c)
    print '----------'
    print 'TEST CASE #4'
    print '----------'
    b = tf.constant(np.arange(13.25, 20.5, dtype=np.float64),
                    shape=[3, 3, 2])

    print 'Input(float64): ' + str(b)
    print '----------'
    a = tensor_to_str(b)
    print 'String: \n' + a

    c = str_to_tensor(a)
    print '----------'
    print 'Tensor from String: \n' + str(sess.run(c))
    print 'Generated Tensor info: ' + str(c)
    sess.close() 
'''