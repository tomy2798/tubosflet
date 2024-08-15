import sqlite3 as sql


class DataManager:
    def __init__(self):
        self.conn = sql.connect('data.db', check_same_thread=False)
    #Manejo de datos de tubos    
    def add_tubo(self, tipo,valor,longitud1,longitud2,espesor):
        query = '''INSERT INTO tubos (tipo,valor,longitud1,longitud2,espesor) 
                VALUES (?,?,?,?,?)'''
        self.conn.execute(query, (tipo,valor,longitud1,longitud2,espesor))
        self.conn.commit()
    
    def get_tubos(self):
        cursor = self.conn.cursor()
        query = '''SELECT * FROM tubos'''
        cursor.execute(query)
        tubos = cursor.fetchall()
        return tubos
    
    def delete_tubo(self,valor):
        query = '''DELETE FROM tubos WHERE valor = ?'''
        self.conn.execute(query,(valor,))
        self.conn.commit()
    
    def update_tubo(self, tipo,valor,longitud1,longitud2,espesor,old_valor):
        query = '''UPDATE tubos SET tipo = ?, valor = ?, longitud1 = ?, longitud2 = ?, espesor = ? WHERE valor = ?'''
        self.conn.execute(query, (tipo,valor,longitud1,longitud2,espesor,old_valor))
        self.conn.commit()
     


    def buscador(self, tipo=None, valor=None, longitud1=None, longitud2=None, espesor=None):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM tubos WHERE 1=1'
        params = []

        if tipo:
            query += ' AND tipo LIKE ?'
            params.append(f'%{tipo}%')
        
        if valor is not None:
            query += ' AND valor = ?'
            params.append(valor)
        
        if longitud1 is not None and longitud2 is not None:
            query += ' AND ((longitud1 = ? AND longitud2 = ?) OR (longitud1 = ? AND longitud2 = ?))'
            params.extend([longitud1, longitud2, longitud2, longitud1])
        elif longitud1 is not None:
            query += ' AND (longitud1 = ? OR longitud2 = ?)'
            params.extend([longitud1, longitud1])
        elif longitud2 is not None:
            query += ' AND (longitud1 = ? OR longitud2 = ?)'
            params.extend([longitud2, longitud2])
        
        if espesor:
            query += ' AND espesor LIKE ?'
            params.append(f'%{espesor}%')

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            print("Resultados encontrados:")
            for row in resultados:
                print(f"tipo: {row[0]}, valor: {row[1]}, longitud1: {row[2]}, longitud2: {row[3]}, espesor: {row[4]}")
        else:
            print("No se encontraron resultados.")
        
        return resultados  
     
    
    #Manejo de datos de espesor
    
    def add_espesor(self,espesor,valor,chapa):
        query = '''INSERT INTO espesor (espesor,valor,chapa) 
                VALUES (?,?,?)'''
        self.conn.execute(query,(espesor,valor,chapa))
        self.conn.commit()
    
    def get_espesores(self):
        cursor = self.conn.cursor()
        query = '''SELECT * FROM espesor'''
        cursor.execute(query)
        espesor = cursor.fetchall()
        return espesor
    
    def delete_espesor(self,valor):
        query = '''DELETE FROM espesor WHERE valor = ?'''
        self.conn.execute(query,(valor,))
        self.conn.commit()
    
    def buscador_espesores(self, espesor=None, valor=None, chapa=None):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM espesor WHERE 1=1'
        params = []
        
        if espesor:
            query += ' AND espesor LIKE ?'
            params.append(f'%{espesor}%')

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            print("Resultados encontrados:")
            for row in resultados:
                print(f"espesor: {row[0]}, valor: {row[1]}, chapa: {row[2]}")
        else:
            print("No se encontraron resultados.")
        
        return resultados
    
    
    
    
    
    
    
    
    def close(self):
        self.conn.close()

#dm = DataManager()
#dm.buscador_espesores(espesor="6,35")
#espesores= dm.get_espesores()

#print(espesores)


