using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace RandomPointsGraph
{
    public partial class MainForm : Form
    {
        private List<PointF> points;
        private Random random;

        public MainForm()
        {
            InitializeComponent();
            InitializeComponents();
        }

        private void InitializeComponents()
        {
            this.Text = "График 1000 случайных точек";
            this.Size = new Size(800, 600);
            this.StartPosition = FormStartPosition.CenterScreen;

            random = new Random();
            points = GenerateRandomPoints(1000);

            // Добавляем обработчик события Paint для отрисовки точек
            this.Paint += MainForm_Paint;
        }

        private List<PointF> GenerateRandomPoints(int count)
        {
            var pointsList = new List<PointF>();

            for (int i = 0; i < count; i++)
            {
                float x = random.Next(0, 101); // X от 0 до 100
                float y = random.Next(0, 101); // Y от 0 до 100
                pointsList.Add(new PointF(x, y));
            }

            return pointsList;
        }

        private void MainForm_Paint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            // Настраиваем преобразование координат
            float scaleX = (this.ClientSize.Width - 40) / 100f;
            float scaleY = (this.ClientSize.Height - 40) / 100f;

            // Рисуем оси
            DrawAxes(g, scaleX, scaleY);

            // Рисуем точки
            DrawPoints(g, scaleX, scaleY);
        }

        private void DrawAxes(Graphics g, float scaleX, float scaleY)
        {
            Pen axisPen = new Pen(Color.Black, 2);
            Font labelFont = new Font("Arial", 8);
            Brush labelBrush = Brushes.Black;

            // Ось X
            g.DrawLine(axisPen, 30, this.ClientSize.Height - 30, this.ClientSize.Width - 10, this.ClientSize.Height - 30);

            // Ось Y
            g.DrawLine(axisPen, 30, 10, 30, this.ClientSize.Height - 30);

            // Подписи осей
            g.DrawString("X", this.Font, labelBrush, this.ClientSize.Width - 20, this.ClientSize.Height - 40);
            g.DrawString("Y", this.Font, labelBrush, 15, 5);

            // Разметка осей
            for (int i = 0; i <= 100; i += 10)
            {
                // Метки на оси X
                int xPos = 30 + (int)(i * scaleX);
                g.DrawLine(Pens.Gray, xPos, this.ClientSize.Height - 35, xPos, this.ClientSize.Height - 25);
                g.DrawString(i.ToString(), labelFont, labelBrush, xPos - 10, this.ClientSize.Height - 25);

                // Метки на оси Y
                int yPos = this.ClientSize.Height - 30 - (int)(i * scaleY);
                g.DrawLine(Pens.Gray, 25, yPos, 35, yPos);
                g.DrawString(i.ToString(), labelFont, labelBrush, 10, yPos - 10);
            }
        }

        private void DrawPoints(Graphics g, float scaleX, float scaleY)
        {
            Brush pointBrush = new SolidBrush(Color.FromArgb(128, Color.Red)); // Полупрозрачные точки
            float pointSize = 3f;

            foreach (var point in points)
            {
                float x = 30 + point.X * scaleX;
                float y = this.ClientSize.Height - 30 - point.Y * scaleY;

                g.FillEllipse(pointBrush, x - pointSize / 2, y - pointSize / 2, pointSize, pointSize);
            }
        }

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);
            this.Invalidate(); // Перерисовываем форму при изменении размера
        }
    }
}