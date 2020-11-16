def message(domain, pk, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료 됩니다. " \
           f"\n\n회원가입 링크 : http://{domain}/api/members/v1/activate/{pk}/{token}/" \
           f"\n\n 갑사합니"
