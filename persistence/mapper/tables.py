

class Tables:

    @staticmethod
    def migrate_users_table() -> str:
        return """
            CREATE TABLE Users (
                id UUID UNIQUE PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                lastname VARCHAR(60) NOT NULL,
                phone_number VARCHAR(10) NOT NULL
            );
        """

    @staticmethod
    def migrate_auth_table() -> str:
        return """
            CREATE TABLE Auth (
                id UUID UNIQUE PRIMARY KEY,
                user_id UUID NOT NULL ,
                email VARCHAR(120) UNIQUE NOT NULL ,
                password VARCHAR(150) NOT NULL ,
                role VARCHAR(25) NOT NULL,
                CONSTRAINT fk_auth_id FOREIGN KEY (user_id) REFERENCES Users(id)
            );
        """

    @staticmethod
    def migrate_pet_table() -> str:
        return """
            CREATE TABLE Pet (
                id UUID UNIQUE PRIMARY KEY,
                user_id UUID NOT NULL,
                name VARCHAR(30),
                specie VARCHAR(10) NOT NULL,
                gender VARCHAR(10) NOT NULL,
                size VARCHAR(10),
                age VARCHAR(10),
                breed VARCHAR(70),
                weight FLOAT,
                live BOOLEAN,
                CONSTRAINT fk_pet_id FOREIGN KEY (user_id) REFERENCES Users(id)

            );
        """

    @staticmethod
    def migrate_medical_history_table() -> str:
        return """
            CREATE TABLE MedicalHistory (
                id UUID UNIQUE PRIMARY KEY,
                issue TEXT,
                pet_id UUID NOT NULL,
                CONSTRAINT fk_mh_id FOREIGN KEY (pet_id) REFERENCES Pet(id)
            );
        """

    @staticmethod
    def migrate_quote_table() -> str:
        return """
            CREATE TABLE Quote (
                id UUID UNIQUE PRIMARY KEY,
                creation_date DATE DEFAULT current_timestamp,
                expiration_date DATE NOT NULL,
                pet_id UUID NOT NULL,
                issue TEXT,
                solved BOOLEAN,
                CONSTRAINT fk_quote_id FOREIGN KEY (pet_id) REFERENCES Pet(id)
            );
        """

    @staticmethod
    def migrate_image_table() -> str:
        return """
            CREATE TABLE Image (
                id UUID UNIQUE PRIMARY KEY,
                image TEXT,
                pet_id UUID,
                medical_history_id UUID,
                CONSTRAINT fk_image_id FOREIGN KEY (pet_id) REFERENCES Pet(id),
                CONSTRAINT fk_image_mh_id FOREIGN KEY (medical_history_id) REFERENCES MedicalHistory(id)
            );
        """

    @staticmethod
    def migrate_document_table() -> str:
        return """
            CREATE TABLE Document (
                id UUID UNIQUE PRIMARY KEY,
                document TEXT,
                medical_history_id UUID,
                CONSTRAINT fk_doc_id FOREIGN KEY (medical_history_id) REFERENCES MedicalHistory(id)
            );
        """

    @staticmethod
    def migration_list() -> list[tuple[str, str]]:
        return [
            (Tables.migrate_users_table(), "Users"),
            (Tables.migrate_auth_table(), "Auth"),
            (Tables.migrate_pet_table(), "Pet"),
            (Tables.migrate_quote_table(), "Quote"),
            (Tables.migrate_medical_history_table(), "MedicalHistory"),
            (Tables.migrate_image_table(), "Image"),
            (Tables.migrate_document_table(), "Document")
        ]
