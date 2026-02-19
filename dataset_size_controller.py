import logging
import shutil
from pathlib import Path
from typing import List


class GitHubDatasetBuilder:
    """
    Cria uma versão reduzida do dataset localizado em qualquer
    pasta 'data/raw' encontrada no projeto.

    O script deve ser executado na raiz do projeto.
    """

    def __init__(self, max_repo_size_mb: int = 90):
        self.project_root = Path.cwd()
        self.max_repo_size_bytes = max_repo_size_mb * 1024 * 1024
        self._configure_logger()

    def _configure_logger(self) -> None:
        self.logger = logging.getLogger("GitHubDatasetBuilder")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def find_raw_directories(self) -> List[Path]:
        """
        Busca recursivamente todas as pastas chamadas 'data/raw'
        dentro do projeto.
        """
        raw_dirs = [
            path for path in self.project_root.rglob("data/raw")
            if path.is_dir()
        ]
        return raw_dirs

    def copy_balanced_files(self, raw_dir: Path) -> None:
        """
        Copia arquivos da pasta raw para github_dataset
        respeitando limite máximo de tamanho.
        """
        self.logger.info(f"Processando diretório: {raw_dir}")

        github_dir = raw_dir.parent / "github_dataset"

        # Limpa pasta destino se existir
        if github_dir.exists():
            shutil.rmtree(github_dir)

        github_dir.mkdir(parents=True, exist_ok=True)

        files = list(raw_dir.rglob("*"))
        files = [f for f in files if f.is_file()]

        if not files:
            self.logger.warning("Nenhum arquivo encontrado.")
            return

        # Ordena por tamanho (menores primeiro)
        files.sort(key=lambda f: f.stat().st_size)

        current_size = 0

        for file in files:
            file_size = file.stat().st_size

            if current_size + file_size > self.max_repo_size_bytes:
                break

            relative_path = file.relative_to(raw_dir)
            destination = github_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file, destination)
            current_size += file_size

        self.logger.info(
            f"Dataset reduzido criado em {github_dir} "
            f"({current_size / (1024*1024):.2f} MB)"
        )

    def execute(self) -> None:
        """
        Executa o processo completo.
        """
        raw_dirs = self.find_raw_directories()

        if not raw_dirs:
            self.logger.warning(
                "Nenhuma pasta 'data/raw' encontrada no projeto."
            )
            return

        for raw_dir in raw_dirs:
            self.copy_balanced_files(raw_dir)

        self.logger.info("Processo finalizado com sucesso.")


if __name__ == "__main__":
    builder = GitHubDatasetBuilder(max_repo_size_mb=90)
    builder.execute()
