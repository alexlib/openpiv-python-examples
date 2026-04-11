# /// script
# requires-python = ">="3.11"
# dependencies = [
#     "marimo",
#     "openpiv",
#     "numpy",
#     "matplotlib",
#     "imageio",
# ]
# ///

import marimo

__generated_with = "0.23.0"
app = marimo.App(layout_file="layouts/test20_windef.grid.json")


@app.cell(hide_code=True)
def _():
    from openpiv import tools, windef

    import marimo as mo

    return mo, tools, windef


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Run the window deformation algorithm

        1. Set the settings and press "Submit"
        2. Press "PIV run"
    """)
    return


@app.cell(hide_code=True)
def _(mo, windef):
    # UI Settings for OpenPIV
    settings = windef.PIVSettings()

    ui_filepath_images = mo.ui.text(value="test20/", label="Image Folder Path")
    ui_save_folder_suffix = mo.ui.text(value="test_20", label="Save Folder Suffix")
    ui_frame_pattern_a = mo.ui.text(value="t_23.png", label="Pattern A")
    ui_frame_pattern_b = mo.ui.text(value="t_24.png", label="Pattern B")
    ui_ROI = mo.ui.dropdown(
        options=["full", "(50,300,50,300)"],
        value="full",
        label="Region of Interest",
    )

    ui_num_iterations = mo.ui.slider(1, 10, value=3, label="Num Iterations")
    ui_windowsizes = mo.ui.multiselect(
        options=[8, 16, 32, 64, 128], value=[64, 32, 16], label="Window Sizes"
    )

    ui_std_threshold = mo.ui.number(value=7, label="STD Threshold")
    ui_median_threshold = mo.ui.number(value=3, label="Median Threshold")

    # Create Form
    piv_form = mo.ui.form(
        mo.ui.array(
            [
                ui_filepath_images,
                ui_save_folder_suffix,
                ui_frame_pattern_a,
                ui_frame_pattern_b,
                ui_ROI,
                ui_num_iterations,
                ui_windowsizes,
                ui_std_threshold,
                ui_median_threshold,
            ]
        ),
        label="PIV Configuration",
    )

    # Create the run button
    run_button = mo.ui.run_button(label="Run PIV")

    # Display UI
    mo.vstack([piv_form, run_button])
    return piv_form, run_button, settings


@app.cell(hide_code=True)
def _(mo, piv_form, run_button, settings, tools, windef):
    import contextlib
    import io

    # Execution cell
    if run_button.value:
        # Update settings from form values
        values = piv_form.value
        settings.filepath_images = values[0]
        settings.save_folder_suffix = values[1]
        settings.frame_pattern_a = values[2]
        settings.frame_pattern_b = values[3]
        settings.ROI = values[4]
        settings.num_iterations = values[5]
        settings.windowsizes = values[6]
        settings.std_threshold = values[7]
        settings.median_threshold = values[8]

        # Capture stdout to find the output file path
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            windef.piv(settings)

        output_text = f.getvalue()

        # Logic to extract the file path (Assuming OpenPIV prints it)
        # You might need to adjust this depending on the actual string format
        # Example: "Results saved to /path/to/field_A0000.txt"
        import re

        match = re.search(r"(/[\w\.\-/]+field_A0000\.txt)", output_text)

        if match:
            result_file = match.group(1)
            tools.display_vector_field(result_file)
        else:
            mo.md(f"PIV run completed. Output: {output_text}")
    else:
        mo.stop("Click the button to run PIV")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
