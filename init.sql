CREATE TABLE al_user_details (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    achievements JSONB,
    address VARCHAR(255),
    educations JSONB,
    email VARCHAR(255),
    first_name VARCHAR(255),
    gender VARCHAR(255),
    interests JSONB,
    languages JSONB,
    last_name VARCHAR(255),
    nationality VARCHAR(255),
    skills JSONB,
    telephone VARCHAR(255),
    work_experiences JSONB,
    generation_id VARCHAR(255),
    user_id VARCHAR(255) UNIQUE
);

ALTER TABLE al_user_details
    OWNER TO postgres;

-- Adding foreign keys
ALTER TABLE al_user_details
    ADD CONSTRAINT fk_generation_id
    FOREIGN KEY (generation_id)
    REFERENCES al_generations (generation_id);

ALTER TABLE al_user_details
    ADD CONSTRAINT fk_user_id
    FOREIGN KEY (user_id)
    REFERENCES al_users (user_id);

INSERT INTO al_user_details (
    id,
    achievements,
    address,
    educations,
    email,
    first_name,
    gender,
    interests,
    languages,
    last_name,
    nationality,
    skills,
    telephone,
    work_experiences,
    generation_id,
    user_id
) VALUES (
    'user1234',
    '{"achievements": ["Won regional math competition", "Published article in scientific journal"]}',
    '123 Elm St, Anytown, Anystate',
    '{"schools": [{"name": "Anytown High", "year": "2015-2019"}]}',
    'user@example.com',
    'Jane',
    'Female',
    '{"hobbies": ["chess", "piano"]}',
    '{"English": "native", "Spanish": "fluent"}',
    'Doe',
    'American',
    '{"programming": ["Python", "Java"]}',
    '555-0123',
    '{"jobs": [{"company": "Tech Corp", "role": "Developer", "years": "2020-2023"}]}',
    'gen789',
    'uid5678'
);
