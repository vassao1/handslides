def detectar_gestos(juntas):
    indicador = juntas[8].y < juntas[6].y
    medio = juntas[12].y < juntas[10].y
    anelar = juntas[16].y < juntas[14].y
    mindinho = juntas[20].y < juntas[18].y
    
    if indicador and medio and not anelar and not mindinho:
        return "VOLTAR"
    
    if indicador and not medio and not anelar and not mindinho:
        return "PASSAR"