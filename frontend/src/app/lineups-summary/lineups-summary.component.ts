import { Component } from '@angular/core';
import { LineupsSummaryResponseComponent } from '../lineups-summary-response/lineups-summary-response.component';

@Component({
  selector: 'lineups-summary-component',
  imports: [LineupsSummaryResponseComponent],
  templateUrl: './lineups-summary.component.html',
  styleUrl: './lineups-summary.component.scss',
})
export class LineupsSummaryComponent {}