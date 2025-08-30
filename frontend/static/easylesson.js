document.addEventListener('DOMContentLoaded', function() {
    const columns = document.querySelectorAll('.column');
    const resizers = document.querySelectorAll('.resizer');
    let currentResizer;

    resizers.forEach(resizer => {
        resizer.addEventListener('mousedown', function(e) {
            currentResizer = e.target;
            let prevX = e.clientX;
            let column = currentResizer.parentElement;
            let nextColumn = column.nextElementSibling;

            // Prevent selecting text while dragging
            document.body.style.userSelect = 'none';

            function mouseMoveHandler(e) {
                if (!currentResizer) return;

                let newX = e.clientX;
                let dx = newX - prevX;

                let columnWidth = column.offsetWidth;
                let nextColumnWidth = nextColumn.offsetWidth;
                let containerWidth = column.parentElement.offsetWidth;

                let newColumnWidth = columnWidth + dx;
                let newNextColumnWidth = nextColumnWidth - dx;

                // Set minimum width for columns
                if (newColumnWidth < 200 || newNextColumnWidth < 200) {
                    return;
                }

                column.style.flexBasis = `${(newColumnWidth / containerWidth) * 100}%`;
                nextColumn.style.flexBasis = `${(newNextColumnWidth / containerWidth) * 100}%`;

                prevX = newX;
            }

            function mouseUpHandler() {
                document.removeEventListener('mousemove', mouseMoveHandler);
                document.removeEventListener('mouseup', mouseUpHandler);
                document.body.style.userSelect = ''; // Restore user selection
                currentResizer = null;
            }

            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        });
    });
});
