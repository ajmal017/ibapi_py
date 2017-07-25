package TestJavaClient;

import java.awt.BorderLayout;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class JDialogBox extends JDialog {

    private boolean m_isOk = false;

    public boolean isOk() {
        return m_isOk;
    }

    public JDialogBox(JFrame parent) {
        super(parent, true);
        
        JPanel buttonPanel = new JPanel();
        JButton btnOk = new JButton("OK");
        JButton btnCancel = new JButton("Cancel");
        
        btnOk.addActionListener(e -> onOk());
        btnCancel.addActionListener(e -> onCancel());

        buttonPanel.add(btnOk);
        buttonPanel.add(btnCancel);
        getContentPane().add(buttonPanel, BorderLayout.SOUTH);
        pack();
    }

    protected void onOk() {
        m_isOk = true;
        
        setVisible(false);
    }
    
    protected void onCancel() {
        m_isOk = false;

        setVisible(false);
    }
    
    @Override
    public void setVisible(boolean b) {
        if (b) {
            m_isOk = false;
        }
        
        super.setVisible(b);
    }
    
}
