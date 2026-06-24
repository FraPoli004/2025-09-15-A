from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(ai, af):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.driverId, d.forename, d.surname
                    from drivers d 
                    join results r on d.driverId = r.driverId join races rc on r.raceId = rc.raceId 
                    where rc.`year` between %s and %s
                    and r.`position` is not null"""

        cursor.execute(query, (ai, af))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(ai, af):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct r1.driverId as d1, r2.driverId as d2, count(*) as peso
                  from results r1, results r2, races rc1, races rc2
                  where  r1.raceId  = rc1.raceId 
                  and r1.raceId = r2.raceId
                  and r2.raceId  = rc2.raceId 
                  and r1.constructorId  = r2.constructorId 
                  and r1.driverId < r2.driverId 
                  and rc1.year >=  %s and rc1.year <= %s and r1.position is not null
                  and rc2.year >=  %s and rc2.year <= %s and r2.position is not null	
                  group by r1.driverId, r2.driverId """
        cursor.execute(query, (ai, af, ai, af))
        for row in cursor:
            result.append((row["d1"], row["d2"], row["peso"]))
        cursor.close()
        conn.close()
        return result

