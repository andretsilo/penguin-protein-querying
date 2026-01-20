from dotenv import dotenv_values

config = dotenv_values(".env")

class StatisticsRepository:
    def __init__(self, collection):
        self.collection = collection

    def annotation_coverage(self):
        # How big is the dataset? How many labeled vs unlabeled proteins? How many
        # annotations?

        pipeline = [
            {
                "$project": {
                    # Create some new temporary document attributes for further analysis
                    "reviewed": 1,  # Take reviewe as is
                    "has_interpro": {  # Check if protein has interpro
                        "$cond": [{"$ne": ["$interpro", ""]}, 1, 0]
                    },
                    "has_ec": {
                        "$cond": [{"$ne": ["$ec_number", ""]}, 1, 0]
                    },
                    "has_gene": {
                        "$cond": [{"$ne": ["$gene_name", ""]}, 1, 0]
                    }
                }
            },
            {
                "$group": {  # For each review status, do some stats
                    "_id": "$reviewed",  # Group key is the reviewed status
                    "total": {"$sum": 1},
                    "with_interpro": {"$sum": "$has_interpro"},
                    "with_ec": {"$sum": "$has_ec"},
                    "with_gene": {"$sum": "$has_gene"}
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))

    def interpro_group_size(self):

        # Group size per Interpro
        # We have to split it because one protein usually has several interpro's
        pipeline = [
            {"$match": {"interpro": {"$ne": ""}}},
            {
                "$project": {
                    "interpro_list": {"$split": ["$interpro", ";"]}  # Split by ;
                }
            },
            {"$unwind": "$interpro_list"},  # Unravel the list
            {
                "$group": {
                    "_id": "$interpro_list",
                    "protein_count": {"$sum": 1}
                }
            },
            {"$sort": {"protein_count": -1}},
            {"$limit": 20}  # Only take maximum 20
        ]

        return list(self.collection.aggregate(pipeline))

    def ec_group_size(self):
        # Same we did for interpro, just for EC number

        pipeline = [
            {"$match": {"ec_number": {"$ne": ""}}},
            {
                "$group": {
                    "_id": "$ec_number",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]

        return list(self.collection.aggregate(pipeline))

    def sequence_length(self):
        # Length of sequence: Reviewed vs. unreviewed

        pipeline = [
            {
                "$project": {
                    "reviewed": 1,
                    "seq_len": {"$strLenCP": "$sequence"}  # $strLenCP calculates
                    # length of string, basically number of UTF-8 points
                }
            },
            {
                "$group": {
                    "_id": "$reviewed",
                    "min_len": {"$min": "$seq_len"},
                    "max_len": {"$max": "$seq_len"},
                    "avg_len": {"$avg": "$seq_len"}
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))