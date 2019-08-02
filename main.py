import os
import chardet

from sys import exit

def Main():
    instructions()
    strTables = input("3) Digite o nome das tabelas(Ex: estoque;clientes): ")
    print("\n")

    newScripts = []
    sqlFiles = getListSqlFiles()
    
    arrayTables = strTables.split(';')

    for table in arrayTables:
        newScripts = getTableScript(table, sqlFiles)

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
def getTableScript(tableName, sqlFiles):
    newFiles = []
    scriptsPath = os.getcwd() + "/scripts"

    for sqlFile in sqlFiles:
        rawdata = open(sqlFile, 'rb').read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']

        keepSaving = False
        endOfTable = False

        for line in open(sqlFile, 'r', encoding=charenc):
            if keepSaving == True:
                if "Table structure for table" in line:
                    tableFile.close()
                    keepSaving = False
                    endOfTable = True
                    break;
                elif "-- T" in line or "-- D" in line or "--" not in line:
                    tableFile.write(line)
            else:
                stringToVerify = "Table structure for table `" + tableName + "`"
                if stringToVerify in line:
                    if os.path.exists(scriptsPath) == False:
                        os.mkdir(scriptsPath)

                    tableFile = open(scriptsPath + "/" + tableName + ".sql", "w")
                    tableFile.write(line)
                    keepSaving = True

                    newFiles.append(tableName + ".sql")

        if endOfTable == True:
            endOfTable = False
            break;

    return newFiles

def instructions():
    print("\n")
    print("######################################")
    print("######### Extract SQL Script #########")
    print("######################################")
    print("\n")
    print("1) Crie uma pasta chamada 'bkp'")
    print("2) Extraia os arquivos do backup dentro da pasta 'bkp'")

Main()