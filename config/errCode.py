def errors(errCode):
    err_dict = {
        0: ("OP_ERR_NONE", "정상"),
        -10: ("OP_ERR_FAIL", "실패"),
        -100: ("OP_ERR_LOGIN", "사용자정보교환실패"),
        -101: ("OP_ERR_CONNECT", "서버접속실패"),
        -102: ("OP_ERR_VERSION", "버전처리실패"),
    }
    result = err_dict[errCode]
    return result