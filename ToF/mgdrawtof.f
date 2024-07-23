*                                                                      *
*=== mgdraw ===========================================================*
*                                                                      *
      SUBROUTINE MGDRAW ( ICODE, MREG )

      INCLUDE 'dblprc.inc'
      INCLUDE 'dimpar.inc'
      INCLUDE 'iounit.inc'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 2003-2019:  CERN & INFN                            *
*     All Rights Reserved.                                             *
*                                                                      *
*     MaGnetic field trajectory DRAWing: actually this entry manages   *
*                                        all trajectory dumping for    *
*                                        drawing                       *
*                                                                      *
*     Created on   01 March 1990   by        Alfredo Ferrari           *
*                                              INFN - Milan            *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'caslim.inc'
      INCLUDE 'comput.inc'
      INCLUDE 'sourcm.inc'
      INCLUDE 'fheavy.inc'
      INCLUDE 'flkstk.inc'
      INCLUDE 'genstk.inc'
      INCLUDE 'mgddcm.inc'
      INCLUDE 'paprop.inc'
      INCLUDE 'quemgd.inc'
      INCLUDE 'sumcou.inc'
      INCLUDE 'trackr.inc'
*
      DIMENSION DTQUEN ( MXTRCK, MAXQMG )
*
      CHARACTER*20 FILNAM
      LOGICAL LFCOPE
      SAVE LFCOPE
      DATA LFCOPE / .FALSE. /
*
*----------------------------------------------------------------------*
*                                                                      *
*     Icode = 1: call from Kaskad                                      *
*     Icode = 2: call from Emfsco                                      *
*     Icode = 3: call from Kasneu                                      *
*     Icode = 4: call from Kashea                                      *
*     Icode = 5: call from Kasoph                                      *
*                                                                      *
*----------------------------------------------------------------------*
*                                                                      *
      IF ( .NOT. LFCOPE ) THEN
         LFCOPE = .TRUE.
c          IF ( KOMPUT .EQ. 2 ) THEN
c             FILNAM = '/'//CFDRAW(1:8)//' DUMP A'
c          ELSE
c             FILNAM = CFDRAW
c          END IF
c          OPEN ( UNIT = IODRAW, FILE = FILNAM, STATUS = 'NEW', FORM =
c      &          'UNFORMATTED' )
      END IF
c       WRITE (IODRAW) NTRACK, MTRACK, JTRACK, SNGL (ETRACK),
c      &               SNGL (WTRACK)
c       WRITE (IODRAW) ( SNGL (XTRACK (I)), SNGL (YTRACK (I)),
c      &                 SNGL (ZTRACK (I)), I = 0, NTRACK ),
c      &               ( SNGL (DTRACK (I)), I = 1, MTRACK ),
c      &                 SNGL (CTRACK)
*  +-------------------------------------------------------------------*
*  |  Quenching is activated
      IF ( LQEMGD ) THEN
         IF ( MTRACK .GT. 0 ) THEN
            RULLL  = ZERZER
            CALL QUENMG ( ICODE, MREG, RULLL, DTQUEN )
c            WRITE (IODRAW) ( ( SNGL (DTQUEN (I,JBK)), I = 1, MTRACK ),
c     &                         JBK = 1, NQEMGD )
         END IF
      END IF
*  |  End of quenching
*  +-------------------------------------------------------------------*
      RETURN
*
*======================================================================*
*                                                                      *
*     Boundary-(X)crossing DRAWing:                                    *
*                                                                      *
*     Icode = 1x: call from Kaskad                                     *
*             19: boundary crossing                                    *
*     Icode = 2x: call from Emfsco                                     *
*             29: boundary crossing                                    *
*     Icode = 3x: call from Kasneu                                     *
*             39: boundary crossing                                    *
*     Icode = 4x: call from Kashea                                     *
*             49: boundary crossing                                    *
*     Icode = 5x: call from Kasoph                                     *
*             59: boundary crossing                                    *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY BXDRAW ( ICODE, MREG, NEWREG, XSCO, YSCO, ZSCO )
cc***********************************************************
cc If a neutron (jtrack=8) cross the boudary then record on file
cc MREG == BEAMLINE REG, NEWREG == DETECTOR REG
cc***********************************************************
      IF (JTRACK.EQ.8) THEN
        IF ((MREG.EQ.3).AND.(NEWREG.EQ.2)) THEN
          CALL GEOR2N ( MREG, MRGNAM, IERR1 )
          CALL GEOR2N ( NEWREG, NRGNAM, IERR2 )
            WRITE(32,1005) JTRACK, ETRACK-AM(JTRACK),
     &        ATRACK, WTRACK
        ENDIF
      ENDIF
1005  FORMAT (1(I4,2x), 3(ES13.3,2x))
      RETURN
*
*======================================================================*
*                                                                      *
*     Event End DRAWing:                                               *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY EEDRAW ( ICODE )
      RETURN
*
*======================================================================*
*                                                                      *
*     ENergy deposition DRAWing:                                       *
*                                                                      *
*     Icode = 1x: call from Kaskad                                     *
*             10: elastic interaction recoil                           *
*             11: inelastic interaction recoil                         *
*             12: stopping particle                                    *
*             13: pseudo-neutron deposition                            *
*             14: escape                                               *
*             15: time kill                                            *
*             16: recoil from (heavy) bremsstrahlung                   *
*     Icode = 2x: call from Emfsco                                     *
*             20: local energy deposition (i.e. photoelectric)         *
*             21: below threshold, iarg=1                              *
*             22: below threshold, iarg=2                              *
*             23: escape                                               *
*             24: time kill                                            *
*     Icode = 3x: call from Kasneu                                     *
*             30: target recoil                                        *
*             31: below threshold                                      *
*             32: escape                                               *
*             33: time kill                                            *
*     Icode = 4x: call from Kashea                                     *
*             40: escape                                               *
*             41: time kill                                            *
*             42: delta ray stack overflow                             *
*     Icode = 5x: call from Kasoph                                     *
*             50: optical photon absorption                            *
*             51: escape                                               *
*             52: time kill                                            *
*                                                                      *
*======================================================================*
*                                                                      *
      ENTRY ENDRAW ( ICODE, MREG, RULL, XSCO, YSCO, ZSCO )
c       IF ( .NOT. LFCOPE ) THEN
c          LFCOPE = .TRUE.
c          IF ( KOMPUT .EQ. 2 ) THEN
c             FILNAM = '/'//CFDRAW(1:8)//' DUMP A'
c          ELSE
c             FILNAM = CFDRAW
c          END IF
c          OPEN ( UNIT = IODRAW, FILE = FILNAM, STATUS = 'NEW', FORM =
c      &          'UNFORMATTED' )
c       END IF
c       WRITE (IODRAW)  0, ICODE, JTRACK, SNGL (ETRACK), SNGL (WTRACK)
c       WRITE (IODRAW)  SNGL (XSCO), SNGL (YSCO), SNGL (ZSCO), SNGL (RULL)
c *  +-------------------------------------------------------------------*
c *  |  Quenching is activated : calculate quenching factor
c *  |  and store quenched energy in DTQUEN(1, jbk)
c       IF ( LQEMGD ) THEN
c          RULLL = RULL
c          CALL QUENMG ( ICODE, MREG, RULLL, DTQUEN )
c *     |  Back from QUENMG, the RULLL quantity does no longer embed
c *     |  the WSCRNG statistical weight
c          WRITE (IODRAW) ( SNGL (DTQUEN(1, JBK)), JBK = 1, NQEMGD )
c       END IF
c *  |  end quenching
*  +-------------------------------------------------------------------*
      RETURN
*
*======================================================================*
*                                                                      *
*     SOurce particle DRAWing:                                         *
*                                                                      *
*======================================================================*
*
      ENTRY SODRAW
c       IF ( .NOT. LFCOPE ) THEN
c          LFCOPE = .TRUE.
c          IF ( KOMPUT .EQ. 2 ) THEN
c             FILNAM = '/'//CFDRAW(1:8)//' DUMP A'
c          ELSE
c             FILNAM = CFDRAW
c          END IF
c          OPEN ( UNIT = IODRAW, FILE = FILNAM, STATUS = 'NEW', FORM =
c      &          'UNFORMATTED' )
c       END IF
c       WRITE (IODRAW) -NCASE, NPFLKA, NSTMAX, SNGL (TKESUM),
c      &                SNGL (WEIPRI)
c *  +-------------------------------------------------------------------*
c *  |  (Radioactive) isotope: it works only for 1 source particle on
c *  |  the stack for the time being
c       IF ( ILOFLK (NPFLKA) .GE. 100000 .AND. LRADDC (NPFLKA) ) THEN
c          IARES  = MOD ( ILOFLK (NPFLKA), 100000  )  / 100
c          IZRES  = MOD ( ILOFLK (NPFLKA), 10000000 ) / 100000
c          IISRES = ILOFLK (NPFLKA) / 10000000
c          IONID  = ILOFLK (NPFLKA)
c          WRITE (IODRAW) ( IONID,SNGL(-TKEFLK(I)),
c      &                    SNGL (WTFLK(I)), SNGL (XFLK (I)),
c      &                    SNGL (YFLK (I)), SNGL (ZFLK (I)),
c      &                    SNGL (TXFLK(I)), SNGL (TYFLK(I)),
c      &                    SNGL (TZFLK(I)), I = 1, NPFLKA )
c *  |
c *  +-------------------------------------------------------------------*
c *  |  Patch for heavy ions: it works only for 1 source particle on
c *  |  the stack for the time being
c       ELSE IF ( ABS (ILOFLK (NPFLKA)) .GE. 10000 ) THEN
c          IONID = ILOFLK (NPFLKA)
c          CALL DCDION ( IONID )
c          WRITE (IODRAW) ( IONID,SNGL(TKEFLK(I)+AMNHEA(-IONID)),
c      &                    SNGL (WTFLK(I)), SNGL (XFLK (I)),
c      &                    SNGL (YFLK (I)), SNGL (ZFLK (I)),
c      &                    SNGL (TXFLK(I)), SNGL (TYFLK(I)),
c      &                    SNGL (TZFLK(I)), I = 1, NPFLKA )
c *  |
c *  +-------------------------------------------------------------------*
c *  |  Patch for heavy ions: ???
c       ELSE IF ( ILOFLK (NPFLKA) .LT. -6 ) THEN
c          WRITE (IODRAW) ( IONID,SNGL(TKEFLK(I)+AMNHEA(-ILOFLK(NPFLKA))),
c      &                    SNGL (WTFLK(I)), SNGL (XFLK (I)),
c      &                    SNGL (YFLK (I)), SNGL (ZFLK (I)),
c      &                    SNGL (TXFLK(I)), SNGL (TYFLK(I)),
c      &                    SNGL (TZFLK(I)), I = 1, NPFLKA )
c *  |
c *  +-------------------------------------------------------------------*
c *  |
c       ELSE
c          WRITE (IODRAW) ( ILOFLK(I), SNGL (TKEFLK(I)+AM(ILOFLK(I))),
c      &                    SNGL (WTFLK(I)), SNGL (XFLK (I)),
c      &                    SNGL (YFLK (I)), SNGL (ZFLK (I)),
c      &                    SNGL (TXFLK(I)), SNGL (TYFLK(I)),
c      &                    SNGL (TZFLK(I)), I = 1, NPFLKA )
c       END IF
c *  |
c *  +-------------------------------------------------------------------*
      RETURN
*
*======================================================================*
*                                                                      *
*     USer dependent DRAWing:                                          *
*                                                                      *
*     Icode = 10x: call from Kaskad                                    *
*             100: elastic   interaction secondaries                   *
*             101: inelastic interaction secondaries                   *
*             102: particle decay  secondaries                         *
*             103: delta ray  generation secondaries                   *
*             104: pair production secondaries                         *
*             105: bremsstrahlung  secondaries                         *
*             110: radioactive decay products                          *
*     Icode = 20x: call from Emfsco                                    *
*             208: bremsstrahlung secondaries                          *
*             210: Moller secondaries                                  *
*             212: Bhabha secondaries                                  *
*             214: in-flight annihilation secondaries                  *
*             215: annihilation at rest   secondaries                  *
*             217: pair production        secondaries                  *
*             219: Compton scattering     secondaries                  *
*             221: photoelectric          secondaries                  *
*             225: Rayleigh scattering    secondaries                  *
*             237: mu pair production     secondaries                  *
*     Icode = 30x: call from Kasneu                                    *
*             300: interaction secondaries                             *
*     Icode = 40x: call from Kashea                                    *
*             400: delta ray  generation secondaries                   *
*     Icode = 50x: call from synstp                                    *
*             500: synchrotron radiation photons from e-/e+            *
*             501: synchrotron radiation photons from other charged    *
*                  particles                                           *
*  For all interactions secondaries are put on GENSTK common (kp=1,np) *
*  but for KASHEA delta ray generation where only the secondary elec-  *
*  tron is present and stacked on FLKSTK common for kp=npflka          *
*                                                                      *
*======================================================================*
*
      ENTRY USDRAW ( ICODE, MREG, XSCO, YSCO, ZSCO )
c       IF ( .NOT. LFCOPE ) THEN
c          LFCOPE = .TRUE.
c          IF ( KOMPUT .EQ. 2 ) THEN
c             FILNAM = '/'//CFDRAW(1:8)//' DUMP A'
c          ELSE
c             FILNAM = CFDRAW
c          END IF
c          OPEN ( UNIT = IODRAW, FILE = FILNAM, STATUS = 'NEW', FORM =
c      &          'UNFORMATTED' )
c       END IF
* No output by default:
      RETURN
*=== End of subrutine Mgdraw ==========================================*
      END

