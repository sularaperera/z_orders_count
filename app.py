import streamlit as st

st.set_page_config(page_title="Z Orders Count", layout="wide")

st.title("📄 Z Orders Count")
st.write(
    "Upload one or more `.txt` files to extract number of distinct Z orders."
)

# File uploader
uploaded_files = st.file_uploader(
    "Upload .txt Files",
    type=["txt"],
    accept_multiple_files=True
)

if uploaded_files:
    distinct_orders = set()

    st.info(f"Found {len(uploaded_files)} file(s) to process.")

    for uploaded_file in uploaded_files:
        try:
            # Read file content
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()

            # Process each line
            for line in lines:
                # Filter rows starting with 'I'
                if line.startswith('I'):
                    values = line.strip().split(',')

                    # Extract second value (index 1)
                    if len(values) > 1:
                        order_number = values[1].strip()
                        distinct_orders.add(order_number)

        except Exception as e:
            st.error(f"Error reading file {uploaded_file.name}: {e}")

    # Final results
    total_distinct_orders = len(distinct_orders)

    st.subheader("✅ Final Aggregated Results")

    st.write("### Distinct Order Numbers")
    st.dataframe(sorted(list(distinct_orders)), use_container_width=True)

    st.success(
        f"Total count of distinct order numbers across all files: {total_distinct_orders}"
    )

    # Download results
    csv_content = "OrderNumber\n" + "\n".join(sorted(list(distinct_orders)))

    st.download_button(
        label="⬇ Download Order Numbers",
        data=csv_content,
        file_name="distinct_orders.csv",
        mime="text/csv"
    )

else:
    st.warning("Please upload one or more .txt files to begin.")