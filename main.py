#Abre el archivo de texto
archive = open("prueba.txt", "r")

"""
Crea una lista por cada de los terminos que se deben tener en cuenta a 
la hora de analizar el código:
variable_list: es un arreglo que guarda todas las variables que han sido declaradas
                durante la ejecución del código.
procedure_list: es un arreglo que guarda todos los procedimientos que han sido
                declarados duarante la ejecución del código.
parameter_list: es un arreglo de diccionarios que guarda todos los parametros 
                por procedimiento que han sido pasados a un procedimiento duarante
                la ejecución del código.
keyword_list: es un arreglo que contiene palabras claves para el inicio/fin 
                del programa o de algún procedimiento, y para la declaración
                de variables.
command_list: es un arreglo que contiene todos los comandos posibles.
number_comm_list: es un arreglo que contiene todos los comandos cuyos parametros
                    son numericos.
conditional_list: es un arreglo que contiene keywords sobre condicionales.
loop_list: es un arreglo que contiene keywords sobre ciclos.
conditions_list: es un arreglo que contiene todas las condiciones posibles.
ins_list: es un arreglo que contiene los comandos cuyos parametos son de tipo
            'ins'.
directions_list: es un arreglo que contiene todas las posibles direcciones.
cardinal_list: es un arreglo que contiene los puntos cardinales.

"""
variable_list = []

procedure_list = []

parameter_list = []

keyword_list = ["PROG", "GORP", "var", "PROC", "CORP"]

command_list = ["walk", "jump", "jumpTo", "veer", "look", "drop", "grab", "get", "free", "pop", "walk"]

number_comm_list = ["jump", "drop", "grab", "get", "free", "pop"]

conditional_list = ["if", "else", "fi"]

loop_list = ["while", "do", "od"]

conditions_list = ["isfacing", "isValid", "canWalk", "not"]

ins_list = ["walk", "jump", "grab", "pop", "pick", "free", "drop"]

directions_list = ["front", "right", "left", "back"]

cardinal_list = ["north","south", "west","east"]

numbers = "1234567890"

#Lee la primera linea del archivo
line = archive.readline().strip()

#Comprueba si 'PROG' esta al inicio del archivo de código
if "PROG" in line:

    #Lee la siguiente linea de código
    line = archive.readline()

    #Establece la condición de que mientras no sea haya una linea vacia se siga leyendo el archivo
    while line != "":
        current_line = line

        #Comprueba si la palabra clave 'var' para la declaración de variables esta presente
        if "var" in current_line:

            #Comprueba si tambien ';' esta presente, puesto que es necesario para cualquier declaración
            if ";" in current_line:

                #Elimina los espacios de la linea; quita las comas y semicolons; vuelve es string un arreglo
                #Se ignora la primera posicion que corresponde a 'var'.
                for char in current_line.strip().replace(",","").replace(";", "").split()[1:]:
                    
                    #Teniendo en cuenta de que solo quedan varibales, se agragan a la lista de variables
                    variable_list.append(char)
            else:
                print("Variable assignation must end with a ';' character")    
                break

        #Comprueba si la palabra clave 'PROC' para la declaración de procedimientos esta presente
        if "PROC" in current_line:

            #Crea una lista temporal para guardar los parametros del procedimiento
            parameterProc_listTemp = []

            for char in current_line.strip().split()[1:]:

                #El primer caracter corresponde al nombre del procedimiento
                proc_name = char

                #Se guarda en la lista de procedimiento
                procedure_list.append(proc_name)
                break

            #Revisa que haya parentesis de inicio y de fin
            if "(" in current_line and ")" in current_line:

                #Crea el diccionario de guardara los parametros por procedimiento
                proc_diccParameter = {
                    proc_name : []
                }

                for char in current_line.strip().replace("(","").replace(")","").replace(",","").split()[2:]:

                    #Teniendo en cuenta de que solo quedan parametros, se agragan al diccionario
                    proc_diccParameter[proc_name].append(char)

                    #Tambien se agregan a la lista temporal de parametros
                    parameterProc_listTemp.append(char)

                #Se agrega el diccionario a la lista de general de parametros
                parameter_list.append(proc_diccParameter)
            else:
                print("Parameters must be into brackets")
                break

            #Lee la siguiente linea del archivo para revisar el bloque de instrucciones del prcedimiento
            line = archive.readline()

            #Comprueba si hay un corchete que abra el bloque de instrucciones
            if "{" in line:

                #Crea unos pivotes para luego comprobar si por cada instrucción hay un semicolon
                num_semicolon = 0
                num_commands = 0

                #Lee la siguiente linea del archivo (Revisar si es necesaria o se puede quitar)
                line = archive.readline()

                #Crea un loop para que se lea el interior del bloque de instrucciones tras el primer corchete
                while "}" not in line:
                    
                    line = archive.readline()

                    #Revisa si exiten comandos dentro del bloque de instrucciones
                    for command in command_list:
                        if command in line.strip().split()[0]:
                            if "(" in line and ")" in line:
                                num_commands += 1
                                for char in line.strip().replace("(","").replace(")","").replace(",","").split()[1]:

                                    #Revisa que los parametros pasados al comando hayan sido definidos como variables 
                                    # o pasados como parametros el procedimiento, de paso revisa que termine en 
                                    # semicolon
                                    if char in variable_list or char in parameterProc_listTemp or char == ";":
                                        pass
                                    else:
                                        print(char + " is not defined")
                                        break
                                if ";" in line:
                                    num_semicolon += 1
                            else:
                                print("Command's parameters must be into brackets")
                                break
                    
                    #Revisa si existe un loop dentro del bloque de instrucciones
                    if "while" in line.strip().split()[0]:

                        #Revisa que exista un numero coherente de parentesis y corchetes, no asegura que este sintacticamente bien pero meh..
                        if line.count("(") == 3 and line.count(")") and line.count("{") == 1 and line.count("}") == 1:
                            temp_line = line.strip().replace("(","").replace(")","").replace(",","").replace("{","").replace("}","").split()

                            #Revisa lo que esta dentro del while sea una condición y que todo termine con 'od'
                            if temp_line[1] in conditions_list and temp_line[-1] == "od":

                                #Revisa por cada posible condición que lo que se le pase por parametro este previamente declarado
                                # o que corresponde al tipo de dato esperado
                                if temp_line[1] == "canWalk":
                                    if temp_line[2] in cardinal_list or temp_line[2] in directions_list:
                                        if temp_line[3] in numbers or temp_line[3] in variable_list or temp_line[3] in parameter_list:
                                            pass
                                    else:
                                        print("Invalid parameters for the condition canWalk")
                                        break
                                elif temp_line[1] == "isfacing":
                                    if temp_line[2] in cardinal_list:
                                        pass
                                    else:
                                        print("Invalid parameters for the condition isfacing")
                                        break
                                elif temp_line[1] == "isValid":
                                    if temp_line[2] in ins_list and temp_line[3] in numbers or temp_line[3] in variable_list or temp_line[3] in parameter_list:
                                        pass
                                    else:
                                        print("Invalid parameters for the condition isValid")
                                        break
                                elif temp_line[1] == "not":
                                    if temp_line[2] in conditions_list:
                                        pass
                                    else:
                                        print("Invalid parameters for the condition not")
                                        break

                                #Revisa a donde comienza el 'do' para empezar a revisar lo que se ejecuta si la condición se cumple
                                do_index = temp_line.index("do")

                                #Revisa que sea un comando lo que vaya a ejecutar
                                if temp_line[do_index + 1] in command_list:

                                    #Revisa por cada posible comando que lo que se le pase por parametro este previamente declarado
                                    # o que corresponde al tipo de dato esperado
                                    if temp_line[do_index + 1] in number_comm_list:
                                        if temp_line[do_index + 2] in numbers or temp_line[do_index + 2] in variable_list or temp_line[do_index + 2] in parameter_list:
                                            pass
                                        else:
                                            print("Invalid parameters for the commands " + temp_line[do_index + 1])

                                    elif temp_line[do_index + 1] == "jumpTo":
                                        if temp_line[do_index + 2] in numbers or temp_line[do_index + 2] in variable_list or temp_line[do_index + 2] in parameter_list:
                                            if temp_line[do_index + 3] in numbers or temp_line[do_index + 3] in variable_list or temp_line[do_index + 3] in parameter_list:
                                                pass
                                            else:
                                                print("Invalid parameters for the command jumpTo")
                                        else:
                                            print("Invalid parameters for the command jumpTo")

                                    elif temp_line[do_index + 1] == "veer":
                                        if temp_line[do_index + 2] in directions_list:
                                            pass
                                        else:
                                            print("Invalid parameters for the command veer")

                                    elif temp_line[do_index + 1] == "look":
                                        if temp_line[do_index + 2] in cardinal_list:
                                            pass
                                        else:
                                            print("Invalid parameters for the command look")

                                    elif temp_line[do_index + 1] == "walk":
                                        if temp_line[-1] != "od":
                                            if temp_line[do_index + 2] in numbers:
                                                pass
                                            else:
                                                print("Invalid parameters for the command walk")
                                        else:
                                            if temp_line[do_index + 3] in numbers and temp_line[do_index + 2] in cardinal_list or temp_line[do_index + 3] in directions_list:
                                                pass
                                            else:
                                               print("Invalid parameters for the command walk") 

                    #Revisa que el bloque de instrcciones se cierre con un corchete
                    if line.strip() == "{":
                        print("Procedure's block of intructions must be within curly brackets")
                        break
                
                #Revisa que despues de cada instrucción exista un semicolon
                if num_commands != 1:
                    if num_semicolon != num_commands - 1:
                        pass
                    else:
                        print("After every command must be a semicolon")
                        break
            else:
                print("Procedure's block of intructions must be within curly brackets")
                break
            
        line = archive.readline()
else:
    print("No")

print(variable_list)
print(procedure_list)
print(parameter_list)

 