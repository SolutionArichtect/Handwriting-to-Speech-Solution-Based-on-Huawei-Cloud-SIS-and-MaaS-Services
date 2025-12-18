import os
import time
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "huaweicloud-python-sdk-sis-1.8.5"))

def run_test():
    try:
        from src.services.sis_service import SisService
    except Exception as e:
        print("SDK import failed:", str(e))
        print("Please install Huawei SIS SDK before running SDK test.")
        return

    text = "求解方程 x 平方 加 2 x 加 1 等于 0 的根。"
    question_id = f"sdk_{int(time.time())}"
    save_dir = os.path.join("audio_output", "tests")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    output_path = os.path.join(save_dir, f"{question_id}.mp3")

    svc = SisService()
    ok = svc.synthesize(text, output_path, "chinese_xiaoyan_common")
    print("Success:", ok)
    print("Output:", output_path if ok else "")

if __name__ == "__main__":
    run_test()
