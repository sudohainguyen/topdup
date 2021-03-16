import "ag-grid-community/dist/styles/ag-grid.css"
import "ag-grid-community/dist/styles/ag-theme-alpine.css"
import React, { Component } from "react"
import { DupReportList } from "./dub-report-list"
import "./dup-report.css"
import DupReportService from "./dup-report.service"
import HeaderRow from "./header-row"
import Pagination from "./pagination"

class DupReport extends Component {
  constructor(props) {
    super(props)
    this.dupReportService = new DupReportService()

    this.state = {
      userData: props.userData,
      setUserData: props.setUserData,
      simReports: [],
      reportsPerPage: 8,
      loading: false,
      currentPage: 1,
      currentMode: "list"
    }
  }

  componentDidMount = () => {
    this.getData()
  };

  getData = () => {
    const user = this.state.userData && this.state.userData.user
    const userId = user && user.id
    this.setState({ loading: true })
    this.dupReportService.getSimilarityRecords(userId)
      .then(results => {
        this.setState({ loading: false })
        this.setState({ simReports: results })
      })
  };

  render() {
    const { simReports, currentMode, reportsPerPage, loading, currentPage } = this.state

    const indexOfLastReport = reportsPerPage * currentPage
    const indexOfFirstReport = reportsPerPage * (currentPage - 1)
    const currentSimReports = simReports.slice(indexOfFirstReport, indexOfLastReport)
    const paginate = pageNum => this.setState({ currentPage: pageNum })
    const nextPage = () => this.setState({ currentPage: currentPage + 1 })
    const prevPage = () => this.setState({ currentPage: currentPage - 1 })

    const listView = (
      <div className="sim-reports-container">
        <div className="sr-list-with-header">
          <HeaderRow />
          <DupReportList setUserData={this.props.setUserData}
            userData={this.props.userData}
            simReports={currentSimReports}
            loading={loading} />
        </div>
        <Pagination
          reportsPerPage={reportsPerPage}
          totalReports={simReports.length}
          paginate={paginate}
          prevPage={prevPage}
          nextPage={nextPage}
          currentPage={currentPage}
        />
      </div>
    )

    return (
      <div>
        <div className="sologan-container">
          <div className="sologan-heading">Bảo vệ nội dung công sức của bạn</div>
          <div className="sologan-description">Nhận thông báo khi nội dung của bạn bị sao chép.</div>
        </div>
        <div style={{ width: "100%", height: "900px" }}>
          {listView}
        </div>
        <div className="sologan-bottom-container">
          <div className="sologan-bottom">
            Bạn muốn trở thành tình nguyện viên của topDup? <br /> Hoặc đăng ký nhận thông báo khi website bị sao chép.
          </div>
          <div className="sologan-bottom">
            <button type="button" className="btn btn-volunteer layout-cell">
              Nộp Đơn TNV
            </button>
            <button type="button" className="btn btn-register-bottom">
              Đăng Ký WEBSITE
            </button>
          </div>
        </div>
      </div>
    )
  }
}

export default DupReport
