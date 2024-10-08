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
						SELECT MAX_PROMO_AMOUNT INTO MAX_AMOUNT FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
						SELECT DISCOUNT_PERCENTAGE INTO PROMO_PERCENTAGE FROM PROMO WHERE PROMO_CODE_NO LIKE R.PROMO_CODE_NO_ID;
						NEW_PAY_AMOUNT := (OLD_PAY_AMOUNT - (OLD_PAY_AMOUNT * (PROMO_PERCENTAGE/100)));
						DIFF := OLD_PAY_AMOUNT - NEW_PAY_AMOUNT;
						IF DIFF < MAX_AMOUNT THEN
								UPDATE PAYMENT SET NET_AMOUNT = NEW_PAY_AMOUNT WHERE PAYMENT_ID LIKE PAY_ID;
								EXIT;
						ELSE
								UPDATE PAYMENT SET NET_AMOUNT = OLD_PAY_AMOUNT - MAX_AMOUNT  WHERE PAYMENT_ID LIKE PAY_ID;
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

SHOW ERRORS ;
SHOW ERRORS PROCEDURE SET_PAYMENT;