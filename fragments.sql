INSERT INTO "user"
(id_user, name_user, email_user, password_hash, password_salt)
VALUES
(1, 'John', 'john@email.com', '$2b$12$gIcSbXQrWqMHTFhbcNOguOQhSNDDq.nQpuX25Fgfy4HKrrIScnaWm', '$2b$12$gIcSbXQrWqMHTFhbcNOguO'),
(2, 'Jane', 'jane@email.com', 's$$2b$12$6e2DSOJwq.Z/pz8LawWPH.5xl3RDDPuAFerF7Pi1SdOeeS.fy.Nmy', '$2b$12$6e2DSOJwq.Z/pz8LawWPH.');

DELETE FROM user
;

INSERT INTO project
(id_project, name_project)
VALUES
(1, 'Project Crew-Verve'),
(2, 'Project Google Cloud'),
(3, 'Project Azure'),
(4, 'Project AWS');

INSERT INTO user_project
(user_id, project_id)
VALUES
(1, 1),
(1, 2),
(2, 2),
(2, 3);

--1 = active, 0 = inactive
INSERT INTO survey
(id_survey, start_date, end_date, name_survey, active, mood, rating, participation, id_project)
VALUES
(1, '2023-01-01 16:00:48.225987', '2023-02-01 16:00:48.225987', 'Project Crew-Verve enero 2023', 0, 0, 0, 0, 1),
(2, '2023-03-01 16:00:48.225987', '2023-04-01 16:00:48.225987', 'Project Google Cloud marzo 2023', 1, 1, 0, 0, 2),
(3, '2023-02-01 16:00:48.225987', '2023-03-01 16:00:48.225987', 'Project Crew-Verve febrero 2023', 0, 0, 0, 0, 1),
(4, '2023-03-01 16:00:48.225987', '2023-04-01 16:00:48.225987', 'Project Crew-Verve marzo 2023', 1, 0, 0, 0, 1),
(5, '2023-02-01 16:00:48.225987', '2023-03-01 16:00:48.225987', 'Project Google Cloud febrero 2023', 0, 0, 0, 0, 2),
(6, '2023-01-01 16:00:48.225987', '2023-02-01 16:00:48.225987', 'Project Google Cloud enero 2023', 0, 0, 0, 0, 2);

DELETE FROM survey
;

-- 1 = completed, 0 = not completed
INSERT INTO survey_ticket
(user_id, survey_id, completed)
VALUES
(1, 1, 1),
(1, 2, 0),
(1, 4, 0);

INSERT INTO survey_answer
(id_survey_answer, id_survey, answers)
VALUES
(1, 1, '1, 1, 1, 1, 1, 1, 1, 1, 1');

SELECT * FROM survey 
WHERE survey.id_project  IN 
(SELECT id_project FROM project WHERE id_project = 1);