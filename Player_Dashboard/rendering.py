# Player_Dashboard/rendering.py

# rendering.py

from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


# Function to handle AgGrid rendering with custom configuration
def render_player_data(player_df):
    # Inject custom JavaScript code for row coloring based on 'WIN' column using hex color codes
    cellStyle = JsCode("""
        function(params) {
            if (params.data.WIN == 'Win') {
                return {'backgroundColor': '#b6e7a2'};  // Custom light green hex color
            } else if (params.data.WIN == 'Lose') {
                return {'backgroundColor': '#f08080'};  // Custom light red hex color
            }
            return {};
        }
    """)

    # Configure grid options for AgGrid
    gb = GridOptionsBuilder.from_dataframe(player_df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Pagination for large datasets
    gb.configure_side_bar()  # Enable sidebar filters
    gb.configure_default_column(editable=True, filter=True, resizable=True)  # Columns are editable and filterable
    gb.configure_grid_options(domLayout='autoHeight')  # Automatically adjusts height of the grid

    # Set custom column widths
    gb.configure_columns(
        ['Kills', 'Deaths', 'Assists', 'KDA', 'CSPM'], 
        width=80  # Example: Adjust width of these columns
    )
    
    # Apply the custom cell style for row coloring
    gridOptions = gb.build()
    gridOptions['defaultColDef']['cellStyle'] = cellStyle

    # Display the editable table using AgGrid
    return AgGrid(
        player_df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=True,
        theme="streamlit",  
        allow_unsafe_jscode=True,  
        enable_enterprise_modules=True,
        height=400,
        width='200%',
    )
