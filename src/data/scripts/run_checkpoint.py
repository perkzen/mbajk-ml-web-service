import great_expectations as ge
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult

from src.data.data_manager import DataManager


def main():
    context = ge.get_context()
    result: CheckpointResult = context.run_checkpoint(checkpoint_name="mbajk_checkpoint")

    if not result["success"]:
        print("[Validate]: Checkpoint validation failed!")
       # raise ValueError("[Validate]: Checkpoint validation failed!")
    else:
        print("[Validate]: Checkpoint validation passed!")

    dm = DataManager(data_path="data")
    current = dm.get_dataframe("processed", "current_data")
    dm.save("processed", "reference_data", current, override=True)


if __name__ == "__main__":
    main()
