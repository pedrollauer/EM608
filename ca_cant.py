mesh = LIRE_MAILLAGE(FORMAT='MED',
                     UNITE=20)

model = AFFE_MODELE(AFFE=_F(MODELISATION='POU_D_T',
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=mesh)

elemprop = AFFE_CARA_ELEM(MODELE=model,
                          POUTRE=_F(CARA=('R', ),
                                    GROUP_MA=('Group_1', ),
                                    SECTION='CERCLE',
                                    VALE=(0.1, )))

mater = DEFI_MATERIAU(ELAS=_F(E=210000000000.0,
                              NU=0.3,
                              RHO=7850.0))

fieldma0 = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),
                                 TOUT='OUI'),
                         MODELE=model)

load = AFFE_CHAR_MECA(DDL_IMPO=_F(DRX=0.0,
                                  DRY=0.0,
                                  DRZ=0.0,
                                  DX=0.0,
                                  DY=0.0,
                                  DZ=0.0,
                                  GROUP_NO=('engaste', )),
                      MODELE=model)

load0 = AFFE_CHAR_MECA(FORCE_NODALE=_F(FZ=-10.0,
                                       GROUP_NO=('carga', )),
                       MODELE=model)

reslin = MECA_STATIQUE(CARA_ELEM=elemprop,
                       CHAM_MATER=fieldma0,
                       EXCIT=(_F(CHARGE=load),
                              _F(CHARGE=load0)),
                       MODELE=model)

Stress = CALC_CHAMP(CONTRAINTE=('SIEF_ELGA', ),
                    CRITERES=('SIEQ_NOEU', ),
                    RESULTAT=reslin)

IMPR_RESU(FORMAT='MED',
          RESU=_F(RESULTAT=Stress),
          UNITE=80)
