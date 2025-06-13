# TASK #

# Design and develop a service that allows us to detect palindromes.

Palindrome examples:
* In English: "Able was I ere I saw Elba"
* In Spanish: "Dábale arroz a la zorra el abad"

# Take into account the following considerations:

- This service must be exposed using a REST API with JSON that allows us to:
  - Detects if a random string is a palindrome from a language field and a text field.
  - List all the detections on the system, allowing filters by date and language.
  - Get the results of one palindrome detection.
  - Remove a detection.

- The allowed languages are (choose any of them):
  1. Rust, with actix-web. 
  2. Python, with fast-api (preferred) or flask. 
  3. C++ 14+

- Use docker and docker-compose. Architecture is up to you.
- The application should be tested as well. Code coverage is important.
- The project should contain a README and be uploaded to GitHub/GitLab/Bitbucket.
- The submitted code, design, and architecture should be production-ready.
