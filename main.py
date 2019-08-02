import os
import chardet

from sys import exit
from chardet.universaldetector import UniversalDetector

def Main():
    instructions()
    strTables = input("3) Digite o nome das tabelas(Ex: estoque;clientes): ")
    print("\n")

    newScripts = []
    sqlFiles = getListSqlFiles()

    newScripts = getTableScript(strTables.split(';'), sqlFiles)

    if len(newScripts) > 0:
        print("Arquivo(s) gerado(s) com sucesso e salvos dentro da pasta 'scripts'!")
    else:
        print("Nenhum arquivo gerado.")


#Array com nome dos arquivos .sql
def getListSqlFiles():
    sqlFiles = []

    if os.path.exists("bkp"):
        for r, d, f in os.walk(os.getcwd() + "/bkp"):
            for file in f:
                if 'database' in file and '.sql' in file:
                    sqlFiles.append(os.path.join(r, file))
    else:
        print("Pasta 'bkp' nao encontrada!")
        exit()        

    if not sqlFiles:
        print("Nenhum arquivo encontrado!")
        exit()

    return sqlFiles

#Gerar arquivo com script da tabela
def getTableScript(arrTables, sqlFiles):
    newFiles = []
    scriptsPath = os.getcwd() + "/scripts"

    print("Lendo arquivos.")

    for sqlFile in sqlFiles:
        if len(arrTables) != len(newFiles):
            encode = getFileEncode(sqlFile)

            keepSaving = False
            endOfTable = False

            for line in open(sqlFile, 'r', encoding=encode):
                if keepSaving == True:
                    if "Table structure for table" in line:
                        tableFile.close()
                        keepSaving = False
                        endOfTable = True
                        print("OK")
                    elif "-- T" in line or "-- D" in line or "--" not in line:
                        tableFile.write(line)
                else:
                    stringToVerify = "Table structure for table `"

                    if stringToVerify in line:
                        tableToVerify = line
                        tableToVerify = tableToVerify.replace('-- Table structure for table `', '').replace('`', '').strip()

                        try:
                            if arrTables.index(tableToVerify) >= 0:
                                if os.path.exists(scriptsPath) == False:
                                    os.mkdir(scriptsPath)

                                print("Extraindo tabela " + tableToVerify + "...")
                                tableFile = open(scriptsPath + "/" + tableToVerify + ".sql", "w")
                                tableFile.write(line)
                                keepSaving = True

                                newFiles.append(tableToVerify + ".sql")
                        except ValueError:
                            pass

            if endOfTable == True:
                endOfTable = False

    return newFiles

def instructions():
    print("######################################")
    print("######### Extract SQL Script #########")
    print("######################################")
    print("\n")
    print("1) Crie uma pasta chamada 'bkp'")
    print("2) Extraia os arquivos do backup dentro da pasta 'bkp'")


def getFileEncode(fileName):
    detector = UniversalDetector()
    detector.reset()

    for line in open(fileName, 'rb'):
        detector.feed(line)
        if detector.done: 
            break

    detector.close()
    return detector.result['encoding']

Main()