--function to calculate age
CREATE OR REPLACE FUNCTION AGE(D_ID IN VARCHAR2)
RETURN NUMBER IS
		BIRTH_DATE DATE;
    D_AGE NUMBER;
BEGIN
		SELECT DATE_OF_BIRTH INTO BIRTH_DATE
		FROM PERSON
		WHERE PERSON_ID = D_ID;
		D_AGE := TRUNC(MONTHS_BETWEEN(SYSDATE, BIRTH_DATE)/12, 0);
		RETURN D_AGE;
END;
/

--to check age function
BEGIN
	DBMS_OUTPUT.PUT_LINE(AGE('13'));
END;
/

--trigger to update rating of a driver after he occurs an accident
CREATE OR REPLACE TRIGGER RATING_CHANGE
    AFTER INSERT
    ON ACCIDENT
DECLARE
    D_ID VARCHAR2(50);
		D_RATING NUMBER;
BEGIN
    SELECT DRIVER_ID INTO D_ID FROM ACCIDENT WHERE REPORT_ID = (SELECT MAX(TO_NUMBER(REPORT_ID)) FROM ACCIDENT);
    SELECT RATING INTO D_RATING FROM PERSON WHERE PERSON_ID LIKE D_ID;
		UPDATE PERSON SET RATING = (D_RATING - (0.1*D_RATING)) WHERE PERSON_ID LIKE D_ID;
END;
/

--procedure to set payment
CREATE OR REPLACE PROCEDURE SET_PAYMENT(U_ID IN VARCHAR2,PAY_ID IN VARCHAR2) IS
		STATUS VARCHAR2(20);
		PROMO_ID VARCHAR2(50);
		MAX_AMOUNT NUMBER;
		OLD_PAY_AMOUNT NUMBER;
		NEW_PAY_AMOUNT NUMBER;
		PROMO_PERCENTAGE NUMBER;
		DIFF NUMBER;
BEGIN
		SELECT NET_AMOUNT INTO OLD_PAY_AMOUNT FROM PAYMENT WHERE PAYMENT_ID LIKE PAY_ID;
		FOR R IN (SELECT PROMO_CODE_NO_ID FROM GETS WHERE USER_ID LIKE U_ID)
		LOOP
	      SELECT PROMO_STATUS INTO STATUS FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
				IF STATUS LIKE 'ACTIVE' THEN
						SELECT PROMO_CODE_NO INTO PROMO_ID FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
						SELECT MAX_PROMO_AMOUNT INTO MAX_AMOUNT FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
						SELECT DISCOUNT_PERCENTAGE INTO PROMO_PERCENTAGE FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
						NEW_PAY_AMOUNT := (OLD_PAY_AMOUNT - (OLD_PAY_AMOUNT * (PROMO_PERCENTAGE/100)));
						DIFF := OLD_PAY_AMOUNT - NEW_PAY_AMOUNT;
						IF DIFF < MAX_AMOUNT THEN
								UPDATE PAYMENT SET NET_AMOUNT = NEW_PAY_AMOUNT WHERE PAYMENT_ID LIKE PAY_ID;
								UPDATE PAYMENT SET PROMO_CODE_ID = PROMO_ID WHERE PAYMENT_ID LIKE PAY_ID;
								EXIT;
						ELSE
								UPDATE PAYMENT SET NET_AMOUNT = OLD_PAY_AMOUNT - MAX_AMOUNT WHERE PAYMENT_ID LIKE PAY_ID;
								UPDATE PAYMENT SET PROMO_CODE_ID = PROMO_ID WHERE PAYMENT_ID LIKE PAY_ID;
								EXIT;
						END IF;
				END IF; 
		END LOOP;
END ;
/

				
BEGIN
	SET_PAYMENT('6','2');
END;
/

--function to calculate rating
CREATE OR REPLACE FUNCTION CALCULATE_RATING(D_ID IN VARCHAR2, RATED NUMBER)
RETURN NUMBER IS
		PERSON_RATED NUMBER;
		OLD_RATING NUMBER;
    NEW_RATING NUMBER;
BEGIN
		SELECT RATING INTO OLD_RATING
		FROM PERSON
		WHERE PERSON_ID = D_ID;
		SELECT NO_OF_PERSON_RATED INTO PERSON_RATED
		FROM PERSON
		WHERE PERSON_ID = D_ID;
		NEW_RATING := ((OLD_RATING * PERSON_RATED) + RATED)/(PERSON_RATED + 1);
		NEW_RATING := ROUND(NEW_RATING, 2);
		UPDATE PERSON SET NO_OF_PERSON_RATED = NO_OF_PERSON_RATED + 1 WHERE PERSON_ID = D_ID;
		RETURN NEW_RATING;
END;
/

--to check calculate rating function
BEGIN
	DBMS_OUTPUT.PUT_LINE(CALCULATE_RATING('17',4.5));
END;
/

--trigger to update choose table
CREATE OR REPLACE TRIGGER UPDATE_CHOOSE
    AFTER INSERT
    ON TRIP
DECLARE
    U_ID VARCHAR2(50);
		D_ID VARCHAR2(50);
		T_ID VARCHAR2(50);
BEGIN
    SELECT DRIVER_ID INTO D_ID FROM TRIP WHERE TRIP_ID = (SELECT MAX(TO_NUMBER(TRIP_ID)) FROM TRIP);
		SELECT USER_ID INTO U_ID FROM TRIP WHERE TRIP_ID = (SELECT MAX(TO_NUMBER(TRIP_ID)) FROM TRIP);
    SELECT TRANS_ID INTO T_ID FROM TRANSPORT WHERE DRIVER_ID = D_ID;
		INSERT INTO CHOOSE VALUES (U_ID,T_ID);
END;
/

--trigger to add promo for a user
CREATE OR REPLACE TRIGGER ADD_PROMO
    AFTER INSERT
    ON TRIP
DECLARE
    U_ID VARCHAR2(50);
		PR_ID VARCHAR2(50);
		COUNT_TRIP NUMBER;
		LAST_TRIP_TIME DATE;
BEGIN
		COUNT_TRIP := 0;
		SELECT PROMO_CODE_NO INTO PR_ID FROM PROMO WHERE PROMO_CODE_NO = (SELECT MAX(TO_NUMBER(PROMO_CODE_NO)) FROM PROMO);
		SELECT USER_ID INTO U_ID FROM TRIP WHERE TRIP_ID = (SELECT MAX(TO_NUMBER(TRIP_ID)) FROM TRIP);
		SELECT START_TIME INTO LAST_TRIP_TIME FROM TRIP WHERE TRIP_ID = (SELECT MAX(TO_NUMBER(TRIP_ID)) FROM TRIP);
		PR_ID := PR_ID + 1;
		FOR R IN (SELECT START_TIME FROM TRIP WHERE USER_ID = U_ID)
		LOOP
	      IF TRUNC((LAST_TRIP_TIME - R.START_TIME), 0) < 7  THEN
						COUNT_TRIP := COUNT_TRIP+1; 
				END IF; 
		END LOOP;
		IF COUNT_TRIP >= 4 THEN
				INSERT INTO PROMO VALUES (PR_ID,10,100,10,'ACTIVE',LAST_TRIP_TIME,LAST_TRIP_TIME+7);
				INSERT INTO GETS VALUES (U_ID,PR_ID);
		ELSIF COUNT_TRIP > 0 AND COUNT_TRIP < 4 THEN
				INSERT INTO PROMO VALUES (PR_ID,10,50,10,'ACTIVE',LAST_TRIP_TIME,LAST_TRIP_TIME+7);
				INSERT INTO GETS VALUES (U_ID,PR_ID);
		END IF;
END;
/

--SELECT SYSDATE + 7
--FROM DUAL;
--SELECT PROMO_CODE_NO +1 FROM PROMO WHERE PROMO_CODE_NO = (SELECT MAX(TO_NUMBER(PROMO_CODE_NO)) FROM PROMO);
--SHOW ERRORS ;
--SHOW ERRORS PROCEDURE SET_PAYMENT;