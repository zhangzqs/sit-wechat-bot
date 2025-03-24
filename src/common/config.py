from typing import Type, TypeVar
import yaml
from pydantic import BaseModel
import argparse

# 定义一个泛型类型 T，限制为 BaseModel 或其子类
T = TypeVar("T", bound=BaseModel)


def load_config(config_file: str, model: Type[T]) -> T:
    """
    从 YAML 文件加载配置并解析为指定的 Pydantic 模型。

    :param config_file: YAML 配置文件路径
    :param model: Pydantic 模型类
    :return: 解析后的 Pydantic 模型实例
    """
    with open(config_file, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return model(**config_data)


def load_config_from_args(model: Type[T]) -> T:
    parser = argparse.ArgumentParser(description="Load configuration from a YAML file.")
    parser.add_argument(
        "--config", type=str, required=True, help="Path to the YAML configuration file"
    )
    args = parser.parse_args()

    # 加载配置文件
    cfg = load_config(args.config, model)
    return cfg
