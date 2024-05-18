CREATE TABLE students (
  student_id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  title VARCHAR(255),
  skills TEXT[],
  deleted BOOLEAN DEFAULT FALSE  -- Adding a 'deleted' column with a default value of FALSE
);

INSERT INTO students (student_id, name, title, skills, deleted) 
VALUES (8, 'David Anderson', 'Machine Learning Engineer', ARRAY['Python', 'TensorFlow', 'Keras'], FALSE);
