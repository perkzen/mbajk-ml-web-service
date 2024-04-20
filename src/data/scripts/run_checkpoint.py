import great_expectations as ge
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult

from src.data.data_manager import DataManager


def main():
    context = ge.get_context()
    result: CheckpointResult = context.run_checkpoint(checkpoint_name="mbajk_checkpoint")

    if not result["success"]:
        # raise ValueError("[Validate]: Checkpoint validation failed!")
        print("[Validate]: Checkpoint validation failed!")

    print("[Validate]: Checkpoint validation passed!")
    dm = DataManager(data_path="data")
    current_data = dm.get_dataframe(folder="processed", file_name="current_data")
    dm.save(folder="processed", file_name="reference_data", df=current_data, override=True)


if __name__ == "__main__":
    main()
