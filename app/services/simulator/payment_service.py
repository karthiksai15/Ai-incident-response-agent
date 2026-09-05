import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | payment-service | %(message)s",
)

logger = logging.getLogger("payment-service")


def process_payment(payment_id: str):
    logger.info("Payment request received: %s", payment_id)

    time.sleep(0.5)

    logger.info("Payment validation successful: %s", payment_id)

    time.sleep(0.5)

    logger.info("Payment processed successfully: %s", payment_id)

    return {
        "payment_id": payment_id,
        "status": "SUCCESS",
    }


if __name__ == "__main__":
    process_payment("PAY-001")
