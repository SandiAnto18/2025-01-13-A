from database.DB_connect import DBConnect
from model.classification import Classification


class DAO():

    @staticmethod
    def getLocalizations():
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
              select distinct localization
from classification c 
order by c.Localization desc
            """

        cursor.execute(query)
        results = []

        for row in cursor:
            results.append(row["localization"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getClassification(localization):
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                  select c.*
from classification c
where c.Localization = %s
                """

        cursor.execute(query, (localization,))
        results = []

        for row in cursor:
            results.append(Classification(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(localization):
        # RECUPERO TUTTI GLI ANNI DISPONIBILI
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                       SELECT c1.GeneID as c1 , c2.GeneID as c2,
               SUM(DISTINCT g.Chromosome) AS peso

        FROM interactions i, classification c1,
             classification c2, genes g

        -- USO c1 e c2 PER COLLEGARE
        -- SEPARATAMENTE I DUE GENEID DELL'INTERAZIONE
        WHERE c1.GeneID = i.GeneID1
        AND c2.GeneID = i.GeneID2

        AND c1.Localization = %s
        AND c1.Localization = c2.Localization

        -- USO OR PERCHE' DEVO RECUPERARE I CROMOSOMI
        -- SIA DEL PRIMO GENE SIA DEL SECONDO GENE
        AND (g.GeneID = c1.GeneID OR g.GeneID = c2.GeneID)

        GROUP BY c1,c2

                    """

        cursor.execute(query, (localization,))
        results = []

        for row in cursor:
            results.append((row["c1"],row["c2"],row["peso"]))

        cursor.close()
        conn.close()
        return results