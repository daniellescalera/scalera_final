IMPORTANT: 
- This Github Repo is forked from https://github.com/kaw393939/user_management unfortunately, I had to delete my repo, due to a severe nesting error. The only way I could also fix it locally is by deleting my .git. I very much didn't want to because I had over 40 additional commits. I made sure to have over 10 commits for this repo. I put my blood, sweat, and tears (a lot of tears) into this assignment. I put screenshots of my commits including time stamps inside my reflection for this assignment (if you scroll all the way down that's where it will be). 

Feature Added: 
- [tests/test_users/test_user_creation.py::test_login_invalid_email](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_users/test_user_creation.py#L55)


Tests added: 

1. Test Validator
- [tests/test_utils/test_validators.py::test_validate_email_success](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_utils/test_validators.py#L8)
 
 2. Test Create
- [tests/test_services/test_user_service.py::test_create_duplicate_user](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_services/test_user_service.py#L36)

3. Login unverified user
- [tests/test_services/test_user_service.py::test_login_unverified_user](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_services/test_user_service.py#L69)

4. Admin Role Update 
- [tests/test_services/test_user_service.py::test_login_unverified_user](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_services/test_user_service.py#L69)

5. Test Retention Status Code
- [tests/analytics/test_retention.py::test_retention_status_code](https://github.com/daniellescalera/scalera_final/blob/main/tests/analytics/test_retention.py#L6)

6. Test docs is accessible
- [tests/analytics/test_retention.py::test_docs_accessible](https://github.com/daniellescalera/scalera_final/blob/main/tests/analytics/test_retention.py#L14)

7. Test User Creation Success
- [tests/test_users/test_user_creation.py::test_create_user_success](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_users/test_user_creation.py#L6)

8. Test User Creation Duplicate
- [tests/test_users/test_user_creation.py::test_create_duplicate_user](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_users/test_user_creation.py#L18)

9. Test Missing Password
- [tests/test_users/test_user_creation.py::test_create_user_missing_fields](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_users/test_user_creation.py#L30)

10. Test Invalid Email
- [tests/test_users/test_user_creation.py::test_create_user_missing_fields](https://github.com/daniellescalera/scalera_final/blob/main/tests/test_users/test_user_creation.py#L30)


Issues Link: 

## Closed Issues

- [Issue #1 - Add validation tests for user input](https://github.com/daniellescalera/scalera_final/issues/1)
- [Issue #2 - Prevent creating duplicate users](https://github.com/daniellescalera/scalera_final/issues/2)
- [Issue #3 - Block login for unverified users](https://github.com/daniellescalera/scalera_final/issues/3)
- [Issue #4 - Allow Admin to update user roles](https://github.com/daniellescalera/scalera_final/issues/4)
- [Issue #5 - Add error handling for missing fields during user creation](https://github.com/daniellescalera/scalera_final/issues/5)

