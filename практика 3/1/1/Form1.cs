using System;
using System.Drawing;
using System.Windows.Forms;

namespace InstrumentStatusApp
{
    public partial class MainForm : Form
    {
        private Label statusLabel;
        private Label statusValue;
        private Button startButton;
        private Button runButton;
        private Button pauseButton;
        private Button stopButton;
        private PictureBox machinePicture;

        private InstrumentStatus currentStatus = InstrumentStatus.Offline;

        public MainForm()
        {
            InitializeComponent();
            SetupUI();
            UpdateStatusDisplay();
        }

        private void InitializeComponent()
        {
            this.SuspendLayout();

            // Form properties
            this.Text = "Instrument Status Control Panel";
            this.Size = new Size(500, 500);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.White;
            this.MinimumSize = new Size(500, 500);

            this.ResumeLayout(false);
        }

        private void SetupUI()
        {
            // Status Label
            statusLabel = new Label()
            {
                Text = "Instrument Status",
                Location = new Point(20, 20),
                Size = new Size(150, 25),
                Font = new Font("Arial", 12, FontStyle.Bold),
                ForeColor = Color.Black
            };

            // Status Value
            statusValue = new Label()
            {
                Text = "Offline",
                Location = new Point(180, 20),
                Size = new Size(150, 25),
                Font = new Font("Arial", 12, FontStyle.Bold),
                ForeColor = Color.Red
            };

            // Machine Picture Box
            machinePicture = new PictureBox()
            {
                Location = new Point(50, 60),
                Size = new Size(400, 250),
                SizeMode = PictureBoxSizeMode.Zoom,
                BorderStyle = BorderStyle.FixedSingle,
                BackColor = Color.LightGray
            };

            // Create and set machine image (using placeholder graphic)
            CreateMachineImage();

            // Buttons - moved to bottom
            startButton = new Button()
            {
                Text = "Start",
                Location = new Point(50, 350),
                Size = new Size(80, 40),
                BackColor = Color.LightGreen,
                Font = new Font("Arial", 10, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat
            };

            runButton = new Button()
            {
                Text = "Run",
                Location = new Point(150, 350),
                Size = new Size(80, 40),
                BackColor = Color.LightBlue,
                Font = new Font("Arial", 10, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat
            };

            pauseButton = new Button()
            {
                Text = "Pause",
                Location = new Point(250, 350),
                Size = new Size(80, 40),
                BackColor = Color.LightYellow,
                Font = new Font("Arial", 10, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat
            };

            stopButton = new Button()
            {
                Text = "Stop",
                Location = new Point(350, 350),
                Size = new Size(80, 40),
                BackColor = Color.LightCoral,
                Font = new Font("Arial", 10, FontStyle.Bold),
                FlatStyle = FlatStyle.Flat
            };

            // Event handlers
            startButton.Click += StartButton_Click;
            runButton.Click += RunButton_Click;
            pauseButton.Click += PauseButton_Click;
            stopButton.Click += StopButton_Click;

            // Add controls to form
            this.Controls.AddRange(new Control[]
            {
                statusLabel,
                statusValue,
                machinePicture,
                startButton,
                runButton,
                pauseButton,
                stopButton
            });
        }

        private void CreateMachineImage()
        {
            // Create a simple machine drawing as a placeholder
            Bitmap machineImage = new Bitmap(400, 250);
            using (Graphics g = Graphics.FromImage(machineImage))
            {
                g.Clear(Color.White);
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

                // Draw a simple machine representation
                using (Pen blackPen = new Pen(Color.Black, 2))
                using (Pen grayPen = new Pen(Color.Gray, 1))
                using (SolidBrush blueBrush = new SolidBrush(Color.SteelBlue))
                using (SolidBrush silverBrush = new SolidBrush(Color.Silver))
                {
                    // Main machine body
                    g.FillRectangle(silverBrush, 100, 80, 200, 100);
                    g.DrawRectangle(blackPen, 100, 80, 200, 100);

                    // Machine base
                    g.FillRectangle(blueBrush, 80, 180, 240, 30);
                    g.DrawRectangle(blackPen, 80, 180, 240, 30);

                    g.DrawRectangle(blackPen, 120, 90, 60, 30);

                    // Buttons on control panel

                    // Display screen

                    g.DrawRectangle(Pens.White, 200, 90, 80, 30);

                    // Status text on display
                    using (Font statusFont = new Font("Arial", 8))
                    using (SolidBrush textBrush = new SolidBrush(Color.Lime))
                    {
                        g.DrawString("READY", statusFont, textBrush, 210, 98);
                    }

                    // Conveyor belt

                    g.DrawRectangle(blackPen, 50, 210, 300, 10);

                    // Product on conveyor

                    g.DrawRectangle(blackPen, 60, 200, 30, 20);

                    // Machine label
                    using (Font labelFont = new Font("Arial", 10, FontStyle.Bold))
                    {
                    }
                }
            }

            machinePicture.Image = machineImage;
        }

        private void StartButton_Click(object sender, EventArgs e)
        {
            currentStatus = InstrumentStatus.Start;
            UpdateStatusDisplay();
            UpdateMachineImage();
        }

        private void RunButton_Click(object sender, EventArgs e)
        {
            currentStatus = InstrumentStatus.Run;
            UpdateStatusDisplay();
            UpdateMachineImage();
        }

        private void PauseButton_Click(object sender, EventArgs e)
        {
            currentStatus = InstrumentStatus.Pause;
            UpdateStatusDisplay();
            UpdateMachineImage();
        }

        private void StopButton_Click(object sender, EventArgs e)
        {
            currentStatus = InstrumentStatus.Stop;
            UpdateStatusDisplay();
            UpdateMachineImage();
        }

        private void UpdateStatusDisplay()
        {
            statusValue.Text = currentStatus.ToString();

            // Update color based on status
            switch (currentStatus)
            {
                case InstrumentStatus.Offline:
                    statusValue.ForeColor = Color.Red;
                    break;
                case InstrumentStatus.Start:
                    statusValue.ForeColor = Color.Orange;
                    break;
                case InstrumentStatus.Run:
                    statusValue.ForeColor = Color.Green;
                    break;
                case InstrumentStatus.Pause:
                    statusValue.ForeColor = Color.Blue;
                    break;
                case InstrumentStatus.Stop:
                    statusValue.ForeColor = Color.DarkRed;
                    break;
            }
        }

        private void UpdateMachineImage()
        {
            if (machinePicture.Image != null)
            {
                // Создаем новый Bitmap на основе существующего изображения
                Bitmap originalImage = new Bitmap(machinePicture.Image);
                using (Graphics g = Graphics.FromImage(originalImage))
                {
                    // Update display text based on status
                    using (Font statusFont = new Font("Arial", 8, FontStyle.Bold))
                    using (SolidBrush textBrush = new SolidBrush(Color.Lime))
                    using (SolidBrush blackBrush = new SolidBrush(Color.Black)) // ИСПРАВЛЕНИЕ: создаем SolidBrush вместо Brushes.Black
                    {
                        // Clear display area
                        g.FillRectangle(blackBrush, 200, 90, 80, 30); // ИСПРАВЛЕНИЕ: используем созданный brush

                        string statusText = currentStatus switch
                        {
                            InstrumentStatus.Offline => "OFFLINE",
                            InstrumentStatus.Start => "STARTING",
                            InstrumentStatus.Run => "RUNNING",
                            InstrumentStatus.Pause => "PAUSED",
                            InstrumentStatus.Stop => "STOPPED",
                            _ => "READY"
                        };

                        g.DrawString(statusText, statusFont, textBrush, 205, 98);
                    }

                    // Update indicator lights
                    Color startLight = currentStatus == InstrumentStatus.Start ? Color.Orange : Color.Gray;
                    Color runLight = currentStatus == InstrumentStatus.Run ? Color.Green : Color.Gray;
                    Color pauseLight = currentStatus == InstrumentStatus.Pause ? Color.Blue : Color.Gray;

                    // ИСПРАВЛЕНИЕ: используем using для brushes
                    using (SolidBrush startBrush = new SolidBrush(startLight))
                    using (SolidBrush runBrush = new SolidBrush(runLight))
                    using (SolidBrush pauseBrush = new SolidBrush(pauseLight))
                    {
                        g.FillEllipse(startBrush, 130, 95, 8, 8);
                        g.FillEllipse(runBrush, 145, 95, 8, 8);
                        g.FillEllipse(pauseBrush, 160, 95, 8, 8);
                    }
                }

                machinePicture.Image = originalImage;
            }
        }

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);

            // Center buttons horizontally when form is resized
            if (startButton != null)
            {
                int buttonY = this.ClientSize.Height - 100;
                int centerX = this.ClientSize.Width / 2;

                startButton.Location = new Point(centerX - 160, buttonY);
                runButton.Location = new Point(centerX - 80, buttonY);
                pauseButton.Location = new Point(centerX, buttonY);
                stopButton.Location = new Point(centerX + 80, buttonY);

                // Resize picture box
                machinePicture.Size = new Size(this.ClientSize.Width - 100, 250);
                machinePicture.Location = new Point(50, 60);
            }
        }
    }

    public enum InstrumentStatus
    {
        Offline,
        Start,
        Run,
        Pause,
        Stop
    }
}