from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAllAlbums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds)/1000/60 as Durata
                        from album a, track t
                        where a.AlbumId = t.AlbumId 
                        GROUP BY a.AlbumId 
                        HAVING Durata > %s"""

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCTROW t1.AlbumId as a1, t2.AlbumId as a2 
                    FROM track t1, track t2, playlisttrack p1, playlisttrack p2
                    WHERE t2.TrackId = p2.TrackId 
                    and t1.TrackId = p1.TrackId
                    and p2.PlaylistId = p1.PlaylistId
                    and t1.AlbumId < t2.AlbumId """

        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result
