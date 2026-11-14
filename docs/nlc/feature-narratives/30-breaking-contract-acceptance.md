# Breaking-contract acceptance

If a change breaks a contract, the build stays failed until you accept the requirement that allows the break. The compiler keeps the list of callers the break affects. You accept the new requirement, and only then does NLC regenerate the codebase around it. The audit shows the acceptance and the callers, because both are on the record.
