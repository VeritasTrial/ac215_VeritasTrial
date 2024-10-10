from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
