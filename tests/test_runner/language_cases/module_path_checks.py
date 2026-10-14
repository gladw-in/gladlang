"""Module path resolution checks."""

from ..cli_support import (
    expect_equal,
    expect_in,
    expect_startswith,
    make_symlink,
    temporary_directory,
)


def _module_layout(directory):
    root = directory / "root"
    (root / "sub").mkdir(parents=True)
    (directory / "outside").mkdir()
    (root / "ok.glad").write_text("PRINTLN 1\n", encoding="utf-8")
    (root / "sub" / "m.glad").write_text("PRINTLN 2\n", encoding="utf-8")
    (root / "UP.GLAD").write_text("PRINTLN 3\n", encoding="utf-8")
    (root / "data.txt").write_text("text", encoding="utf-8")
    (directory / "outside" / "o.glad").write_text("PRINTLN 4\n", encoding="utf-8")
    return root


def _resolve(source, root, importing_directory=None):
    from gladlang.runtime.modules.path_security import resolve_module_path

    result = resolve_module_path(
        source, str(importing_directory or root), str(root), None, None, None
    )

    return (result.error.details if result.error else None), (
        None if result.error else result.value
    )


def _path_rejects_bad_strings():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        for bad in ("", None, 5, 1.5, ["a.glad"]):
            expect_equal(
                _resolve(bad, root)[0],
                "Import path must be a non-empty string",
                f"{bad!r} is rejected",
            )

        expect_equal(
            _resolve("a\x00b.glad", root)[0], "Invalid import path", "NUL byte"
        )


def _path_rejects_absolute_paths():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        expect_equal(
            _resolve(str(root / "ok.glad"), root)[0],
            "Absolute import paths are not allowed",
            "absolute path",
        )


def _path_requires_glad_extension():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        expect_equal(
            _resolve("data.txt", root)[0],
            "Import path 'data.txt' must point to a '.glad' file",
            "wrong extension",
        )
        expect_equal(_resolve("UP.GLAD", root)[0], None, "extension check ignores case")


def _path_reports_missing_files():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        message = _resolve("missing.glad", root)[0]
        expect_startswith(message, "Module not found: ", "missing file inside the root")
        expect_in("missing.glad", message, "names the file")


def _path_stays_inside_the_root():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        expect_equal(
            _resolve("../outside/o.glad", root)[0],
            "Import path '../outside/o.glad' escapes the module root",
            "existing file outside the root",
        )


def _path_resolves_relative_to_the_importing_file():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        resolved = _resolve("../ok.glad", root, importing_directory=root / "sub")
        expect_equal(resolved[0], None, "no error")
        expect_equal(resolved[1][1], "ok.glad", "cache key is relative to the root")
        expect_equal(
            _resolve("./sub/../ok.glad", root)[1][1],
            "ok.glad",
            "dot segments are normalised",
        )
        expect_equal(_resolve("sub/m.glad", root)[1][1], "sub/m.glad", "nested module")


def _path_blocks_symlink_escape():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        make_symlink(root / "link.glad", directory / "outside" / "o.glad")
        expect_equal(
            _resolve("link.glad", root)[0],
            "Import path 'link.glad' escapes the module root",
            "symlink pointing outside the root",
        )
